import time
import FFBattleSystem


class Equipment:
    def __init__(self):
        self.heroesCanEquip = []
        self.name = ""
        self.weakness = []
        self.resistance = []

    def unequipHero(self, newEquipment, hero):
        while True:
            print("Would you like to replace the {} with the {}?".format(self.name, newEquipment.name, hero))
            time.sleep(0.5)
            print("\t\t1. Yes")
            print("\t\t2. No")
            equipChoice = input().lower()
            if equipChoice == "1":
                hero.equipment.remove(self)
                newEquipment.equipHero(hero)
                FFBattleSystem.playerCurrentInventory.addEquipment(self)
                break
            elif equipChoice == "2":
                break
            else:
                print("That is not a valid response.")
            time.sleep(1)


class Armor(Equipment):
    def __init__(self):
        super().__init__()
        self.armorType = ""
        self.armorValue = 0
        self.weight = 0

    def equipHero(self, hero):
        if not (any(isinstance(hero, heroClass) for heroClass in self.heroesCanEquip)):
            print("{} is unable to wear the {}.".format(hero.name, self.name))
            time.sleep(1)
        elif any(self.armorType == wornArmor.armorType for wornArmor in hero.equipment):
            currentArmor = [wornArmor for wornArmor in hero.equipment if wornArmor.armorType == self.armorType]
            print("{} cannot wear the {} because they are already wearing the {}.".format(hero.name, self.name,
                                                                                          currentArmor[0].name))
            time.sleep(1)
            currentArmor[0].unequipHero(self)
        else:
            print("{} now wears the {}.".format(hero.name, self.name))
            FFBattleSystem.playerCurrentInventory.removeEquipment(self)
            time.sleep(1)
            hero.equipment.append(self)
            hero.armor += self.armorValue
            hero.agility -= self.weight
            hero.weakness.extend(self.weakness)
            hero.resistance.extend(self.resistance)


class Helmet(Armor):
    def __init__(self):
        super().__init__()
        self.armorType = "Helmet"


class LeatherCap(Helmet):
    def __init__(self):
        super().__init__()
        self.armorValue = 2
        self.weight = 1
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.Monk,
                               FFBattleSystem.RedMage, FFBattleSystem.WhiteMage, FFBattleSystem.BlackMage]
        self.name = "Leather Cap"


class MetalHelmet(Helmet):
    def __init__(self):
        super().__init__()
        self.armorValue = 5
        self.weight = 1
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Metal Helmet"


class HeavyHelmet(Helmet):
    def __init__(self):
        super().__init__()
        self.armorValue = 8
        self.weight = 8
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.RedMage]
        self.name = "Heavy Helmet"


class CursedHat(Helmet):
    def __init__(self):
        super().__init__()
        self.armorValue = 5
        self.weight = 1
        self.heroesCanEquip = [FFBattleSystem.RedMage, FFBattleSystem.WhiteMage, FFBattleSystem.BlackMage]
        self.name = "Cursed Hat"
        self.weakness = ["Fire", "Poison"]


class BodyArmor(Armor):
    def __init__(self):
        super().__init__()
        self.armorType = "Armor"


class ThickRobes(BodyArmor):
    def __init__(self):
        super().__init__()
        self.armorValue = 2
        self.weight = 2
        self.heroesCanEquip = [FFBattleSystem.Monk, FFBattleSystem.RedMage, FFBattleSystem.WhiteMage,
                               FFBattleSystem.BlackMage]
        self.name = "Thick Robes"


class LeatherArmor(BodyArmor):
    def __init__(self):
        super().__init__()
        self.armorValue = 5
        self.weight = 8
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.Monk,
                               FFBattleSystem.RedMage]
        self.name = "Leather Armor"


class ChainMail(BodyArmor):
    def __init__(self):
        super().__init__()
        self.armorValue = 13
        self.weight = 15
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Chain Mail"


class ConerianPlateArmor(BodyArmor):
    def __init__(self):
        super().__init__()
        self.armorValue = 22
        self.weight = 20
        self.heroesCanEquip = [FFBattleSystem.Fighter]
        self.name = "Conerian Plate Armor"


class FirebrandArmor(BodyArmor):
    def __init__(self):
        super().__init__()
        self.armorValue = 20
        self.weight = 18
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.RedMage]
        self.name = "Firebrand Armor"
        self.weakness = ["Fire"]
        self.resistance = ["Ice"]


class Gauntlets(Armor):
    def __init__(self):
        super().__init__()
        self.armorType = "Gauntlets"


class ThickGloves(Gauntlets):
    def __init__(self):
        super().__init__()
        self.armorValue = 2
        self.weight = 1
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage,
                               FFBattleSystem.WhiteMage, FFBattleSystem.BlackMage]
        self.name = "Thick Gloves"


class MagicalRing(Gauntlets):
    def __init__(self):
        super().__init__()
        self.armorValue = 4
        self.weight = 0
        self.heroesCanEquip = [FFBattleSystem.RedMage, FFBattleSystem.WhiteMage, FFBattleSystem.BlackMage]
        self.name = "Magical Ring"
        self.weakness = ["Status", "Death"]


class CopperGauntlets(Gauntlets):
    def __init__(self):
        super().__init__()
        self.armorValue = 5
        self.weight = 6
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Copper Gauntlets"


class IronGauntlets(Gauntlets):
    def __init__(self):
        super().__init__()
        self.armorValue = 8
        self.weight = 8
        self.heroesCanEquip = [FFBattleSystem.Fighter]
        self.name = "Copper Gauntlets"


class Shield(Armor):
    def __init__(self):
        super().__init__()
        self.armorType = "Shield"


class SmallShield(Shield):
    def __init__(self):
        super().__init__()
        self.armorValue = 3
        self.weight = 0
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage,
                               FFBattleSystem.WhiteMage, FFBattleSystem.BlackMage]
        self.name = "Small Shield"


class LargeShield(Shield):
    def __init__(self):
        super().__init__()
        self.armorValue = 6
        self.weight = 0
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Large Shield"


class HeavyShield(Shield):
    def __init__(self):
        super().__init__()
        self.armorValue = 8
        self.weight = 4
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Heavy Shield"


class HolyTempleShield(Shield):
    def __init__(self):
        super().__init__()
        self.armorValue = 8
        self.weight = 0
        self.heroesCanEquip = [FFBattleSystem.Monk]
        self.name = "Holy Temple Shield"
        self.weaponType = ""
        self.weakness = ["Status", "Fire"]


class Weapon(Equipment):
    def __init__(self):
        super().__init__()
        self.damageValue = 0
        self.criticalChance = 0
        self.hitRate = 0
        self.contactElement = []

    def equipHero(self, hero):
        if not (any(isinstance(hero, heroClass) for heroClass in self.heroesCanEquip)):
            print("{} is unable to wield the {}.".format(hero.name, self.name))
            time.sleep(1)
        elif any(isinstance(Weapon, equippedWeapon) for equippedWeapon in hero.equipment):
            currentWeapon = [equippedWeapon for equippedWeapon in hero.equipment if isinstance(Weapon, equippedWeapon)]
            print("{} cannot wield the {} because they are already wielding the {}.".format(hero.name, self.name,
                                                                                            currentWeapon[0].name))
            time.sleep(1)
            currentWeapon[0].unequipHero(self)
        else:
            print("{} now wields the {}.".format(hero.name, self.name))
            FFBattleSystem.playerCurrentInventory.removeEquipment(self)
            time.sleep(1)
            hero.equipment.append(self)
            hero.strength += self.damageValue
            hero.criticalChance += self.criticalChance
            hero.hitRate += self.hitRate
            hero.weakness.extend(self.weakness)
            hero.resistance.extend(self.resistance)


class SmallDagger(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 4
        self.criticalChance = 10
        self.hitRate = 15
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage,
                               FFBattleSystem.BlackMage]
        self.name = "Small Dagger"
        self.weaponType = "Knife"


class ObsidianKnife(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 7
        self.criticalChance = 25
        self.hitRate = 10
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.BlackMage]
        self.name = "Obsidian Knife"
        self.weaponType = "Knife"


class BlackAdderDagger(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 8
        self.criticalChance = 30
        self.hitRate = 25
        self.heroesCanEquip = [FFBattleSystem.Thief, FFBattleSystem.BlackMage]
        self.name = "Black Adder Dagger"
        self.weaponType = "Knife"
        self.resistance = ["Death"]


class ShortSword(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 9
        self.criticalChance = 8
        self.hitRate = 5
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Short Sword"
        self.weaponType = "Sword"


class Cutlass(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 12
        self.criticalChance = 6
        self.hitRate = 10
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Cutlass"
        self.weaponType = "Sword"


class LongSword(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 16
        self.criticalChance = 8
        self.hitRate = 14
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.RedMage]
        self.name = "Long Sword"
        self.weaponType = "Sword"


class ShortBow(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 14
        self.criticalChance = 14
        self.hitRate = 6
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage,
                               FFBattleSystem.WhiteMage]
        self.name = "Short Bow"
        self.weaponType = "Bow"


class Longbow(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 12
        self.criticalChance = 8
        self.hitRate = 10
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.WhiteMage]
        self.name = "Longbow"
        self.weaponType = "Bow"


class Crossbow(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 16
        self.criticalChance = 8
        self.hitRate = 4
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.RedMage, FFBattleSystem.WhiteMage]
        self.name = "Crossbow"
        self.weaponType = "Bow"


class Hatchet(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 12
        self.criticalChance = 12
        self.hitRate = 2
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage,
                               FFBattleSystem.BlackMage]
        self.name = "Hatchet"
        self.weaponType = "Axe"


class HandAxe(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 18
        self.criticalChance = 10
        self.hitRate = 2
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Hand Axe"
        self.weaponType = "Axe"


class SharpAxe(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 11
        self.criticalChance = 25
        self.hitRate = 6
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief]
        self.name = "Sharp Axe"
        self.weaponType = "Axe"


class MageStaff(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 7
        self.criticalChance = 8
        self.hitRate = 6
        self.heroesCanEquip = [FFBattleSystem.RedMage, FFBattleSystem.WhiteMage, FFBattleSystem.BlackMage]
        self.name = "Mage Staff"
        self.weaponType = "Staff"


class MorningStar(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 9
        self.criticalChance = 10
        self.hitRate = 5
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.RedMage]
        self.name = "Morning Star"
        self.weaponType = "Staff"


class HolyStaff(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 3
        self.criticalChance = 3
        self.hitRate = 3
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage,
                               FFBattleSystem.WhiteMage, FFBattleSystem.BlackMage]
        self.name = "Holy Staff"
        self.weaponType = "Staff"
        self.resistance = ["Fire", "Lightning", "Ice", "Air", "Death"]


class WarHammer(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 9
        self.criticalChance = 1
        self.hitRate = 5
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.RedMage, FFBattleSystem.WhiteMage]
        self.name = "War Hammer"
        self.weaponType = "Hammer"


class IronHammer(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 11
        self.criticalChance = 5
        self.hitRate = 5
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.WhiteMage]
        self.name = "Iron Hammer"
        self.weaponType = "Hammer"


class ThorHammer(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 12
        self.criticalChance = 8
        self.hitRate = 15
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.WhiteMage]
        self.name = "Thor's Hammer"
        self.weaponType = "Hammer"
        self.contactElement = ["Lightning"]
        self.weakness = ["Air"]


class PoleArm(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 4
        self.criticalChance = 15
        self.hitRate = 4
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Pole Arm"
        self.weaponType = "Spear"


class Javelin(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 10
        self.criticalChance = 15
        self.hitRate = 4
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.Thief, FFBattleSystem.RedMage]
        self.name = "Javelin"
        self.weaponType = "Spear"


class SilverSpear(Weapon):
    def __init__(self):
        super().__init__()
        self.damageValue = 8
        self.criticalChance = 15
        self.hitRate = 6
        self.heroesCanEquip = [FFBattleSystem.Fighter, FFBattleSystem.RedMage]
        self.name = "Silver Spear"
        self.weaponType = "Spear"
        self.resistance = ["Air"]


class EquipmentInstance:
    LEATHER_CAP = LeatherCap()
    HEAVY_HELMET = HeavyHelmet()
    METAL_HELMET = MetalHelmet()
    CURSED_HAT = CursedHat()
    THICK_ROBES = ThickRobes()
    LEATHER_ARMOR = LeatherArmor()
    CHAIN_MAIL = ChainMail()
    CONERIAN_PLATE_ARMOR = ConerianPlateArmor()
    FIREBRAND_ARMOR = FirebrandArmor()
    THICK_GLOVES = ThickGloves()
    MAGICAL_RING = MagicalRing()
    COPPER_GAUNTLETS = CopperGauntlets()
    IRON_GAUNTLETS = IronGauntlets()
    SMALL_SHIELD = SmallShield()
    LARGE_SHIELD = LargeShield()
    HEAVY_SHIELD = HeavyShield()
    HOLY_TEMPLE_SHIELD = HolyTempleShield()
    SMALL_DAGGER = SmallDagger()
    OBSIDIAN_KNIFE = ObsidianKnife()
    BLACK_ADDER_DAGGER = BlackAdderDagger()
    SHORT_SWORD = ShortSword()
    CUTLASS = Cutlass()
    LONG_SWORD = LongSword()
    SHORT_BOW = ShortBow()
    LONGBOW = Longbow()
    CROSSBOW = Crossbow()
    HATCHET = Hatchet()
    HAND_AXE = HandAxe()
    SHARP_AXE = SharpAxe()
    MAGE_STAFF = MageStaff()
    MORNING_STAR = MorningStar()
    HOLY_STAFF = HolyStaff()
    WAR_HAMMER = WarHammer()
    IRON_HAMMER = IronHammer()
    THOR_HAMMER = ThorHammer()
    POLE_ARM = PoleArm()
    JAVELIN = Javelin()
    SILVER_SPEAR = SilverSpear()
