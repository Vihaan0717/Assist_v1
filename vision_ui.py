# vision_ui.py
import cv2
import numpy as np
import mediapipe as mp
import math
import time

# --- HELPER: SMOOTHING ---
class Smoother:
    def __init__(self, alpha=0.5):
        self.x = 0
        self.y = 0
        self.alpha = alpha 

    def update(self, new_x, new_y):
        if self.x == 0 and self.y == 0:
            self.x, self.y = new_x, new_y
        else:
            self.x = (self.alpha * new_x) + ((1 - self.alpha) * self.x)
            self.y = (self.alpha * new_y) + ((1 - self.alpha) * self.y)
        return int(self.x), int(self.y)

# --- VIRTUAL BUTTON ---
class Button:
    def __init__(self, text, pos, size=(100, 50), color=(255, 0, 255)):
        self.text = text
        self.x, self.y = pos
        self.w, self.h = size
        self.color = color
        self.hover_start = 0
        
    def draw(self, img):
        # Draw Button Box
        cv2.rectangle(img, (self.x, self.y), (self.x+self.w, self.y+self.h), self.color, 2)
        cv2.putText(img, self.text, (self.x + 10, self.y + 30), 
                   cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
        
        # Hover Animation
        if time.time() - self.hover_start < 0.2: 
            overlay = img.copy()
            cv2.rectangle(overlay, (self.x, self.y), (self.x+self.w, self.y+self.h), self.color, -1)
            cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

    def is_hovering(self, fx, fy):
        return self.x < fx < self.x + self.w and self.y < fy < self.y + self.h

# --- 3D OBJECT (TRUE 3D) ---
class VirtualObject:
    def __init__(self, x, y, size=60):
        self.x = x
        self.y = y
        self.size = size
        # 3D Cube Coordinates
        self.base_points = [
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]
        ]
        self.current_points = [] 
        self.smoother = Smoother(alpha=0.3)
        self.angle_x = 0.5 # Initial tilt to show depth
        self.angle_y = 0.5 
        self.update_points()

    def update_points(self):
        # Apply Rotation Matrix
        cx, sx = math.cos(self.angle_x), math.sin(self.angle_x)
        cy, sy = math.cos(self.angle_y), math.sin(self.angle_y)
        
        new_points = []
        for p in self.base_points:
            x, y, z = p[0], p[1], p[2]
            
            # Rotate Y
            rx, rz = x*cy + z*sy, z*cy - x*sy
            # Rotate X
            ry, rz = y*cx - rz*sx, y*sx + rz*cx
            
            new_points.append([rx, ry, rz])
        self.current_points = new_points

    def draw(self, img):
        points_2d = []
        # Perspective Projection
        for p in self.current_points:
            f = 400 # Focal length (Depth factor) - Increased for HD
            z = p[2] + 4 # Move away from camera so we don't divide by zero
            
            px = int(p[0] * self.size * 1.5) + self.x
            py = int(p[1] * self.size * 1.5) + self.y
            points_2d.append((px, py))
            cv2.circle(img, (px, py), 4, (0, 255, 255), -1)

        # Draw Edges
        edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
        for i, j in edges:
            cv2.line(img, points_2d[i], points_2d[j], (0, 255, 0), 2)

# --- MAIN UI CLASS ---
class HologramUI:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
        self.mp_draw = mp.solutions.drawing_utils
        self.objects = []
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0
        
        # Position buttons for HD Screen (1280x720)
        self.btn_cube = Button("CUBE", (20, 150), color=(0, 255, 0))
        self.btn_clear = Button("CLEAR", (20, 250), color=(0, 0, 255))
        self.btn_exit = Button("EXIT", (1100, 20), color=(0, 255, 255)) # Moved to top right corner
        self.buttons = [self.btn_cube, self.btn_clear, self.btn_exit]
        
        self.hand_smooth = Smoother(alpha=0.6)

    def start(self):
        cap = cv2.VideoCapture(0)
        
        # --- FORCE HD RESOLUTION ---
        cap.set(3, 1280)
        cap.set(4, 720)
        
        print("🖐️ Advanced AR Active. Drawing disabled near objects.")
        cv2.namedWindow("Jarvis Visual Interface", cv2.WINDOW_NORMAL)

        while True:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            if self.canvas is None or self.canvas.shape[:2] != (h, w):
                self.canvas = np.zeros((h, w, 3), np.uint8)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb_frame)

            finger_x, finger_y = 0, 0
            pinched = False
            
            # STATE FLAGS
            is_hovering_ui = False
            is_near_object = False
            grabbing_object = False

            # Draw Buttons
            for btn in self.buttons:
                btn.draw(frame)

            if result.multi_hand_landmarks:
                for hand_lms in result.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                    
                    raw_x = int(hand_lms.landmark[8].x * w)
                    raw_y = int(hand_lms.landmark[8].y * h)
                    x2 = int(hand_lms.landmark[4].x * w)
                    y2 = int(hand_lms.landmark[4].y * h)
                    
                    # Smooth Finger
                    finger_x, finger_y = self.hand_smooth.update(raw_x, raw_y)

                    # Pinch Logic
                    dist = np.hypot(x2 - raw_x, y2 - raw_y)
                    if dist < 40: pinched = True

            # --- LOGIC FLOW (STRICT PRIORITY) ---

            # 1. Check UI Collision
            for btn in self.buttons:
                if btn.is_hovering(finger_x, finger_y):
                    is_hovering_ui = True
                    btn.hover_start = time.time()
                    if pinched:
                        if btn.text == "EXIT": cap.release(); cv2.destroyAllWindows(); return
                        elif btn.text == "CLEAR": self.objects = []; self.canvas = np.zeros((h, w, 3), np.uint8)
                        elif btn.text == "CUBE": 
                            self.objects.append(VirtualObject(w//2, h//2))
                            time.sleep(0.5)

            # 2. Check Object Collision (Safety Zone)
            for obj in self.objects:
                dist_to_obj = np.hypot(obj.x - finger_x, obj.y - finger_y)
                
                # If hand is within 120px of object, DISABLE DRAWING
                if dist_to_obj < 120:
                    is_near_object = True
                    
                    if pinched:
                        grabbing_object = True
                        obj.x, obj.y = obj.smoother.update(finger_x, finger_y)
                        # Rotate based on movement (Natural feel)
                        obj.angle_y += (finger_x - obj.x) * 0.001
                        obj.angle_x += (finger_y - obj.y) * 0.001
                        obj.update_points()
                    else:
                        # Auto Spin when idle
                        obj.angle_y += 0.02 
                        obj.update_points()
                
                obj.draw(frame)

            # 3. Draw (ONLY if NOT near UI and NOT near Object)
            can_draw = not is_hovering_ui and not is_near_object
            
            if pinched and can_draw and finger_x > 0:
                # Visual Indicator: Blue Circle = Drawing Mode
                cv2.circle(frame, (finger_x, finger_y), 10, (255, 0, 0), -1) 
                
                if self.prev_x == 0 and self.prev_y == 0:
                    self.prev_x, self.prev_y = finger_x, finger_y
                
                # Neon Glow Line (Light Blue)
                cv2.line(self.canvas, (self.prev_x, self.prev_y), (finger_x, finger_y), (255, 255, 0), 15) # Glow
                cv2.line(self.canvas, (self.prev_x, self.prev_y), (finger_x, finger_y), (255, 255, 255), 3) # Core
                
                self.prev_x, self.prev_y = finger_x, finger_y
            else:
                self.prev_x, self.prev_y = 0, 0
                # Visual Indicator: Yellow Circle = Hover Mode
                if finger_x > 0: cv2.circle(frame, (finger_x, finger_y), 8, (0, 255, 255), -1)

            # Composite
            img_gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
            _, img_inv = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY_INV)
            img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
            frame = cv2.bitwise_and(frame, img_inv)
            frame = cv2.add(frame, self.canvas)

            cv2.imshow("Jarvis Visual Interface", frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'): break
            elif key == ord('s'): cv2.imwrite("project_analysis.jpg", frame); print("Snapshot Saved!")

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    ui = HologramUI()
    ui.start()