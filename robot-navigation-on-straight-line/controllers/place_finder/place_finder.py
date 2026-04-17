from controller import Supervisor
import math

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# Get robot node
self_node = robot.getSelf()
translation_field = self_node.getField("translation")

gps = robot.getDevice("gps")
gps.enable(timestep)

MAP = {
    "kitchen": [-1.45, 0.39],
    "main_door": [-8.53, 0.39],
    "table": [-5.12, 0.39]
}

def get_position():
    pos = translation_field.getSFVec3f()
    return pos[0], pos[2]

def set_position(x, z):
    # keep y same
    pos = translation_field.getSFVec3f()
    translation_field.setSFVec3f([x, pos[1], z])

def go_to(target_x, target_z):
    print("Moving to:", target_x, target_z)

    while robot.step(timestep) != -1:

        x, z = get_position()

        dx = target_x - x
        dz = target_z - z

        dist = math.sqrt(dx*dx + dz*dz)

        if dist < 0.2:
            print("Arrived")
            break

        # simple interpolation movement (smooth teleport-style motion)
        step_size = 0.05

        new_x = x + dx * step_size
        new_z = z + dz * step_size

        set_position(new_x, new_z)

# input loop
while robot.step(timestep) != -1:

    for place in MAP:

        print("Going to:", place)

        x, z = MAP[place]
        go_to(x, z)

        # optional pause so you can see movement clearly
        for _ in range(20):
            if robot.step(timestep) == -1:
                break