def count_vehicles(cars):
    traffic = {
        "North": 0,
        "South": 0,
        "East": 0,
        "West": 0
    }
    for car in cars:
        x, y, direction = car[1], car[2], car[3]
        # Count vehicles near the intersection
        if direction == "down" and -50 < y < 220:
            traffic["North"] += 1
        elif direction == "up" and 380 < y < 650:
            traffic["South"] += 1
        elif direction == "right" and -60 < x < 370:
            traffic["West"] += 1
        elif direction == "left" and 530 < x < 960:
            traffic["East"] += 1
    return traffic
def choose_green_direction(traffic, current_direction=None):
    # Check whether any vehicle is approaching
    if max(traffic.values()) == 0:
        return current_direction or "North"
    # Select direction with maximum traffic
    return max(traffic, key=traffic.get)
def explain_decision(traffic, direction):
    return (
        f"{direction} selected because "
        f"{traffic[direction]} vehicles are approaching."
    )


# Testing live vehicle counting

if __name__ == "__main__":

    test_cars = [
        [-1, 405, 100, "down", (0, 150, 255)],
        [-1, 485, 500, "up", (255, 255, 0)],
        [-1, 100, 245, "right", (255, 100, 100)],
        [-1, 700, 335, "left", (255, 255, 255)]
    ]

    traffic = count_vehicles(test_cars)

    print("===== LIVE TRAFFIC COUNT =====")

    for direction, count in traffic.items():
        print(direction, ":", count, "vehicles")

    decision = choose_green_direction(traffic)

    print("\n===== AI DECISION =====")
    print("Selected Direction:", decision)
    print("Signal: GREEN")

    print("\n===== EXPLANATION =====")
    print(explain_decision(traffic, decision))
