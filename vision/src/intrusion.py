import cv2

class IntrusionDetector:

    def __init__(self, boundary_y):
        self.boundary_y = boundary_y
        #Remember prev states
        self.person_states = {}

    def draw_boundary(self, frame):

        _, width = frame.shape[:2]

        cv2.line(
            frame,
            (0, self.boundary_y),
            (width, self.boundary_y),
            (0, 0, 255),
            2
        )

    def get_feet_position(self, box):

        x1,y1, x2, y2 = box

        center_x = int((x1 + x2)/2)
        feet_y = int(y2)

        return center_x, feet_y
    
    def get_state(self, point):
        _, y = point

        if y > self.boundary_y:
            return "inside"

        return "outside"

    def check_intrusion(self, track_id, point):

        current_state = self.get_state(point)

        previous_state = self.person_states.get(track_id)

        # Update state
        self.person_states[track_id] = current_state

        # Detect OUTSIDE -> INSIDE transition
        if previous_state == "outside" and current_state == "inside":
            return True

        return False