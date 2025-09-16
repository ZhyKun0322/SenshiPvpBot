from minecraft.networking.packets import HeldItemChangePacket, AnimationPacket, PlayerPositionAndLookPacket, UseItemPacket, EntityMetadataPacket
from config import MELEE_RANGE, BOW_RANGE, CRIT_JUMP_HEIGHT, LOW_HP, LOW_FOOD
from utils import distance
import time

class CombatSystem:
    def __init__(self, bot):
        self.bot = bot

    def pvp_loop(self, target_pos, _):
        bot_pos = self.bot.spawn_position
        dist = distance(bot_pos, target_pos)

        # Decide action
        if dist > MELEE_RANGE and dist <= BOW_RANGE:
            self.use_bow()
        else:
            self.use_melee(target_pos)

        self.check_bot_health()
        self.use_ender_pearl()

    def use_melee(self, target_pos):
        self.switch_item("sword")
        self.jump()
        self.swing()
        print("[Combat] Melee attack executed.")

    def switch_item(self, item_name):
        slot = 0 if item_name=="sword" else 1
        packet = HeldItemChangePacket()
        packet.slot = slot
        self.bot.safe_send(packet)

    def swing(self):
        if self.bot.entity_id is None:
            return
        packet = AnimationPacket()
        packet.entity_id = self.bot.entity_id
        packet.animation = 0
        self.bot.safe_send(packet)

    def jump(self):
        packet = PlayerPositionAndLookPacket()
        packet.y += CRIT_JUMP_HEIGHT
        packet.on_ground = False
        self.bot.safe_send(packet)

    def use_bow(self):
        self.switch_item("bow")
        packet = UseItemPacket()
        packet.hand = 0
        self.bot.safe_send(packet)
        print("[Combat] Shot bow at target.")

    def check_bot_health(self):
        # Auto-eat golden apple if bot HP low
        if self.bot.health < LOW_HP or self.bot.hunger < LOW_FOOD:
            self.auto_eat()

    def auto_eat(self):
        packet = UseItemPacket()
        packet.hand = 0
        self.bot.safe_send(packet)
        print("[Combat] Eating golden apple.")

    def use_ender_pearl(self):
        # Use pearl only if HP is dangerously low
        if self.bot.health < LOW_HP / 2:
            packet = UseItemPacket()
            packet.hand = 0
            self.bot.safe_send(packet)
            print("[Combat] Threw ender pearl.")
