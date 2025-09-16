from minecraft.networking.packets import HeldItemChangePacket, AnimationPacket, PlayerPositionAndLookPacket, UseItemPacket
from config import MELEE_RANGE, BOW_RANGE, CRIT_JUMP_HEIGHT, LOW_HP, LOW_FOOD, TARGET_LOW_HP
from utils import distance
import time

class CombatSystem:
    def __init__(self, bot):
        self.bot = bot

    def pvp_loop(self, target_pos, target_hp):
        bot_pos = self.bot.spawn_position
        dist = distance(bot_pos, target_pos)

        # Decide action
        if dist > MELEE_RANGE and dist <= BOW_RANGE:
            self.use_bow()
        else:
            self.use_melee(target_pos, target_hp)

        self.auto_eat()
        self.use_ender_pearl(target_hp)

    def use_melee(self, target_pos, target_hp):
        self.switch_item("sword")
        self.jump()
        self.swing()
        if target_hp <= TARGET_LOW_HP:
            print("[Combat] Aggressive melee attack!")

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

    def auto_eat(self):
        packet = UseItemPacket()
        packet.hand = 0
        self.bot.safe_send(packet)
        print("[Combat] Eating golden apple if HP low.")

    def use_ender_pearl(self, target_hp):
        packet = UseItemPacket()
        packet.hand = 0
        self.bot.safe_send(packet)
        print("[Combat] Threw ender pearl.")
