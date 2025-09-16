import time
from minecraft.networking.connection import Connection
from minecraft.networking.packets import ChatPacket, DisconnectPacket, JoinGamePacket
from config import HOST, PORT, USERNAME, OFFLINE_MODE
from utils import distance

from combat import CombatSystem
from movement import MovementSystem
from chat_commands import ChatCommandHandler

class SenshiPvpBot:
    def __init__(self):
        self.username = USERNAME
        self.connection = None
        self.is_fighting = False
        self.target_player = None
        self.alive = True
        self.entity_id = None
        self.health = 20
        self.hunger = 20
        self.players = {}  # {player_name: {'pos':(x,y,z), 'hp':20}}
        self.spawn_position = (0,0,0)

        self.combat = CombatSystem(self)
        self.movement = MovementSystem(self)
        self.chat_commands = ChatCommandHandler(self)

    def connect(self):
        print(f"[+] Connecting to {HOST}:{PORT}")
        try:
            self.connection = Connection(HOST, PORT, username=USERNAME, force_offline=OFFLINE_MODE)
            self.connection.connect()
            self.register_listeners()
            print("[+] Connected!")
        except Exception as e:
            print(f"[!] Connection failed: {e}, retrying in 5s")
            time.sleep(5)
            self.connect()

    def register_listeners(self):
        self.connection.register_packet_listener(self.chat_commands.handle_chat, ChatPacket)
        self.connection.register_packet_listener(self.on_disconnect, DisconnectPacket)
        self.connection.register_packet_listener(self.on_join_game, JoinGamePacket)

    def on_disconnect(self, packet):
        print("[!] Disconnected. Reconnecting...")
        time.sleep(2)
        self.connect()

    def on_join_game(self, packet: JoinGamePacket):
        self.entity_id = packet.entity_id
        print(f"[+] Received entity ID: {self.entity_id}")

    def safe_send(self, packet):
        if self.connection and self.connection.state == 'PLAY':
            self.connection.write_packet(packet)

    def get_player_position(self, player_name):
        if player_name in self.players:
            return self.players[player_name]['pos']
        return None

    def get_player_hp(self, player_name):
        if player_name in self.players:
            return self.players[player_name]['hp']
        return 20  # default

    def run(self):
        self.connect()
        print("[*] Main loop running...")
        try:
            while True:
                if self.alive:
                    if self.is_fighting and self.target_player:
                        target_pos = self.get_player_position(self.target_player)
                        target_hp = self.get_player_hp(self.target_player)
                        if target_pos:
                            self.movement.follow_target(target_pos)
                            self.combat.pvp_loop(target_pos, target_hp)
                        else:
                            # Lost target
                            self.is_fighting = False
                            self.target_player = None
                    else:
                        self.movement.roam()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("[*] Stopped manually.")
            if self.connection:
                self.connection.disconnect()
