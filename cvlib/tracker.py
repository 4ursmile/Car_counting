import math

class LimitQueue:
    def __init__(self, limit = 5):
        self.queue = []
        self.limit = limit
    def push(self, item):
        if len(self.queue) >= self.limit:
            self.queue.pop(0)
        self.queue.append(item)
    def pop(self):
        return self.queue.pop(0)
    def contain(self, item) -> bool:
        return item in self.queue
class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.count = 0
        self.limitq = LimitQueue(5)

    def update(self, objects_rect, liney, acceptable = 5, delta = 25):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get lower center point of new object
        for rect in objects_rect:
            ux, uy, lx, ly = rect
            cx = (ux+lx) // 2
            cy = ly

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
                if cy < liney + acceptable and cy > liney - acceptable and self.limitq.contain(id) == False:
                    self.count+=1;
                    self.limitq.push(id)
                if cy > pt[1]:
                    direction = 1
                else:
                    direction = -1
                if dist < delta:
                    self.center_points[id] = (cx, cy)
                    print(self.center_points)
                    objects_bbs_ids.append([ux, uy, lx, ly, id, direction])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([ux, uy, lx, ly, self.id_count, 0])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id, _ = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids



