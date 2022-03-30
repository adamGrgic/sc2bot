import sc2 
from sc2 import BotAI, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.player import Bot, Computer 




class CompetitiveBot(BotAI):
    NAME: str = "CompetitiveBot"
    """This bot's name"""
    RACE: Race = Race.Protoss
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """

    async def on_start(self):
        print("Game started")
        # Do things here before the game starts

    async def on_step(self, iteration):
        # Populate this function with whatever your bot should do!
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_gateway()


        pass

    async def build_pylons(self):
        if (self.supply_left < 10):
            print('I have less than 10 supply')
            if (self.can_afford(UnitTypeId.PYLON)): 
                print('can afford probe')
                worker_candidates = self.workers.filter(lambda worker: (worker.is_collecting or worker.is_idle) and worker.tag not in self.unit_tags_received_action)
                if (worker_candidates):
                    map_center = self.game_info.map_center
                    position_towards_map_center = self.start_location.towards(map_center, distance=5)
                    placement_position = await self.find_placement(UnitTypeId.PYLON, near=position_towards_map_center, placement_step=1)
                    # Placement_position can be None
                    if placement_position:
                        build_worker = worker_candidates.closest_to(placement_position)
                        build_worker.build(UnitTypeId.PYLON, placement_position)
                
                
                

    async def build_gateway(self):
        if (self.supply_army == 0 and self.can_afford(UnitTypeId.GATEWAY)):
            print('can afford probe')
            worker_candidates = self.workers.filter(lambda worker: (worker.is_collecting or worker.is_idle) and worker.tag not in self.unit_tags_received_action)
            if (worker_candidates):
                map_center = self.game_info.map_center
                position_towards_map_center = self.start_location.towards(map_center, distance=5)
                placement_position = await self.find_placement(UnitTypeId.GATEWAY, near=position_towards_map_center, placement_step=1)
                # Placement_position can be None
                if placement_position:
                    build_worker = worker_candidates.closest_to(placement_position)
                    build_worker.build(UnitTypeId.GATEWAY, placement_position)

    async def build_workers(self):
        nexus = self.townhalls.ready.random
        if (
            self.can_afford(UnitTypeId.PROBE)
            and nexus.is_idle
            and self.workers.amount < self.townhalls.amount *22
        ):
            nexus.train(UnitTypeId.PROBE)


    def on_end(self, result):
        print("Game ended.")
        # Do things here after the game ends
