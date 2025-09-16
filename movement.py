import random
import time
from minecraft.networking.packets import PositionAndLookPacket
from config import ROAM_DELAY, MELEE_RANGE
from utils import distance

class MovementSystem:
    def __init__(self, bot):
        self.bot = bot
        self.spawn_position = bot.spawn_position
        self.roam_radius = 30
        self.yaw = 0
        self.pitch = 0

    def roam(self):
        x = self.spawn_position[0] + random.randint(-self.roam_radius, self.roam_radius)
        z = self.spawn_position[2] + random.randint(-self.roam_radius, self.roam_radius)
        y = self.spawn_position[1]
        self.send_position(x,y,z)
        time.sleep(ROAM_DELAY)

    def follow_target(self, target_pos):
        bot_pos = self.spawn_position
        dist = distance(bot_pos, target_pos)
        if dist > MELEE_RANGE:
            new_x = bot_pos[0] + (target_pos[0]-bot_pos[0])*0.5
            new_z = bot_pos[2] + (target_pos[2]-bot_pos[2])*0.5
            self.send_position(new_x, bot_pos[1], new_z)

    def send_position(self, x,y,z):
        packet = PositionAndLookPacket()
        packet.x, packet.y, packet.z = x,y,z
        packet.yaw, packet.pitch = self.yaw, self.pitch
        packet.on_ground = True
        self.bot.safe_send(packet)
