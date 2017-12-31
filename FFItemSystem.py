import random
import time
import collections
import FFBattleSystem
import FFStatusSystem


class Inventory:
    def __init__(self):
        self.items = collections.OrderedDict()
        self.keyItems = []
        self.equipment = collections.OrderedDict()
        self.gold = 0

    def checkInventory(self):
        for index, itemHeld in enumerate(self.items.keys()):
            print("\t\t{}. {}: {} held  {}".format(index + 1, itemHeld.name, self.items[itemHeld], itemHeld.effect))

    def checkKeyItems(self):
        for index, item in enumerate(self.keyItems):
            print("\t\t{}. {}  {}".format(index + 1, item.name, item.effect))

    def checkEquipment(self):
        for index, equip in enumerate(self.equipment.keys()):
            print("\t\t{}. {}: ({} held)".format(index + 1, equip.name, self.equipment[equip]))

    def checkGold(self):
        print("Gold: {}".format(self.gold))

    def addItem(self, item):
        if item in self.items.keys() and self.items[item] < 99:
            self.items[item] += 1
        elif item in self.items.keys():
            print("You cannot hold another {}.".format(item.name))
        else:
            self.items[item] = 1

    def addKeyItem(self, item):
        if item not in self.keyItems:
            self.keyItems.append(item)

    def addEquipment(self, equip):
        if equip in self.equipment.keys() and self.equipment[equip] < 99:
            self.equipment[equip] += 1
        elif equip in self.equipment.keys():
            print("You cannot hold another {}.".format(equip.name))
        else:
            self.equipment[equip] = 1

    def removeItem(self, item):
        if self.items[item] == 1:
            self.items.pop(item)
        else:
            self.items[item] -= 1

    def removeEquipment(self, equip):
        if self.equipment[equip] == 1:
            self.equipment.pop(equip)
        else:
            self.equipment[equip] -= 1

    def useItem(self, allTargets):
        if not self.items:
            print("Your inventory is empty.")
            time.sleep(1)
            return False
        while True:
            print("Choose which item you'd like to use.")
            time.sleep(1)
            # Prints all available targets, and the indices to each available target
            self.checkInventory()
            print("\t\tc. Cancel")
            targetChosen = input()
            # Returns the chosen index, or None if the player chose to cancel the action
            if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(self.items):
                itemSelected = list(self.items.keys())[int(targetChosen) - 1]
                targetChosenBoolean = itemSelected.chooseItemTarget(allTargets)
                if targetChosenBoolean:
                    self.removeItem(itemSelected)
                    return True
                else:
                    return False
            elif targetChosen.lower() == "c":
                return False
            else:
                print("That is not a valid response.")
            time.sleep(1)


class Item:
    def __init__(self):
        self.name = ""
        self.effect = ""
        self.targetParty = "Enemy"
        self.targetQuantity = "All"
        self.power = 0

    def chooseItemTarget(self, listOfTargets):
        if self.targetParty == "Ally":
            targetList = [hero for hero in listOfTargets if isinstance(hero, FFBattleSystem.Hero)]
        else:
            targetList = [enemy for enemy in listOfTargets if isinstance(enemy, FFBattleSystem.Enemy)]
        while True:
            if self.targetQuantity == "One":
                print("Choose who you'd like to use the {} on.".format(self.name))
                time.sleep(1)
                for index, target in enumerate(targetList):
                    print("\t\t{}. {}".format(index + 1, target.name))
                print("\t\tc. Cancel")
                targetOfItem = input()
                # Returns the chosen index, or None if the player chose to cancel the action
                if targetOfItem.isnumeric() and 0 < int(targetOfItem) <= len(targetList):
                    self.resolveItem(targetList[int(targetOfItem) - 1])
                    return True
                elif targetOfItem.lower() == "c":
                    return False
                else:
                    print("That is not a valid response.")
            else:
                if self.targetParty == "Ally":
                    targetAffiliation = "your party"
                else:
                    targetAffiliation = "the enemies"
                print("Use the {} on {}?".format(self.name, targetAffiliation))
                time.sleep(0.5)
                print("\t\t1. Yes")
                print("\t\t2. No")
                useItemBoolean = input()
                if useItemBoolean == "1":
                    self.resolveItem(targetList)
                    return True
                elif useItemBoolean == "2":
                    return False
                else:
                    print("That is not a valid response.")
            time.sleep(1)

    def resolveItem(self, target):
        pass


class HealingItems(Item):
    def __init__(self):
        super().__init__()
        self.targetParty = "Ally"
        self.targetQuantity = "One"

    def resolveItem(self, target):
        if self.targetQuantity == "One":
            print("{} uses the {}.".format(target.fullName, self.name))
            healHPValue = random.randint(self.power, 2 * self.power)
            time.sleep(1)
            FFBattleSystem.Character.printAmountHealed(target, healHPValue)
            FFBattleSystem.Character.healCharacter(target, healHPValue)
            FFBattleSystem.Character.printCurrentHP(target)
        else:
            for character in target:
                healHPValue = random.randint(self.power, 2 * self.power)
                FFBattleSystem.Character.printAmountHealed(character, healHPValue)
                FFBattleSystem.Character.healCharacter(character, healHPValue)
                FFBattleSystem.Character.printCurrentHP(character)


class Potion(HealingItems):
    def __init__(self):
        super().__init__()
        self.power = 25
        self.name = "Potion"
        self.effect = "(Restores low HP to one hero)"


class HighPotion(HealingItems):
    def __init__(self):
        super().__init__()
        self.power = 45
        self.name = "High Potion"
        self.effect = "(Restores moderate HP to one hero)"


class PartyPotion(HealingItems):
    def __init__(self):
        super().__init__()
        self.power = 20
        self.name = "Party Potion"
        self.effect = "(Restores low HP to all heroes)"
        self.targetQuantity = "All"


class StatusCuringItems(Item):
    def __init__(self):
        super().__init__()
        self.targetParty = "Ally"
        self.targetQuantity = "One"
        self.status = []

    def resolveItem(self, target):
        if self.targetQuantity == "One":
            print("{} uses the {}.".format(target.name, self.name))
            time.sleep(1)
            for statusEffect in self.status:
                newStatus = statusEffect.createNewStatusInstance()
                self.applyStatus(newStatus(), target)
        else:
            for character in target:
                for statusEffect in self.status:
                    newStatus = statusEffect.createNewStatusInstance()
                    self.applyStatus(newStatus(), character)

    def applyStatus(self, statusEffect, target):
        if statusEffect.isCharacterAlreadyAffectedByStatus(target):
            target.status = [currentStatus for currentStatus in target.status if
                             currentStatus.name != statusEffect.name]
            print("{}'s body is purged of its {}.".format(target.fullName, statusEffect.name))
        else:
            targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
            print("But the {} had no effect on {}.".format(self.name, targetName))
        time.sleep(1)


class Antidote(StatusCuringItems):
    def __init__(self):
        super().__init__()
        self.name = "Antidote"
        self.effect = "(Cures a hero affected by poison)"
        self.status = [FFStatusSystem.Poison]


class SageSalt(StatusCuringItems):
    def __init__(self):
        super().__init__()
        self.name = "Sage Salt"
        self.effect = "(Cures a hero affected by confusion)"
        self.status = [FFStatusSystem.Confusion]


class BrightHerb(StatusCuringItems):
    def __init__(self):
        super().__init__()
        self.name = "Bright Herb"
        self.effect = "(Cures a hero affected by paralysis)"
        self.status = [FFStatusSystem.Paralysis]


class SoftSalve(StatusCuringItems):
    def __init__(self):
        super().__init__()
        self.name = "Soft Salve"
        self.effect = "(Cures a hero affected by stone)"
        self.status = [FFStatusSystem.Stone]


class StatusInflictingItems(Item):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"
        self.targetQuantity = "One"
        self.status = ""
        self.itemAccuracy = 0

    def resolveItem(self, target):
        if self.targetQuantity == "One":
            targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
            print("The {} hits {}.".format(self.name, targetName))
            time.sleep(1)
            itemToHit = self.itemAccuracy - target.magicDef
            randomCheckToHit = random.randint(1, 200)
            if randomCheckToHit <= itemToHit:
                for statusEffect in self.status:
                    newStatus = statusEffect.createNewStatusInstance()
                    self.applyStatus(newStatus(), target)
            else:
                print("But the {} had no effect on {}.".format(self.name, targetName))
                time.sleep(1)
        else:
            for character in target:
                targetName = "enemy " + character.name if isinstance(character, FFBattleSystem.Enemy) else\
                    character.name
                itemToHit = self.itemAccuracy - character.magicDef
                randomCheckToHit = random.randint(1, 200)
                if randomCheckToHit <= itemToHit:
                    for statusEffect in self.status:
                        newStatus = statusEffect.createNewStatusInstance()
                        self.applyStatus(newStatus(), character)
                else:
                    print("But the {} had no effect on {}.".format(self.name, targetName))
                    time.sleep(1)

    def applyStatus(self, statusEffect, target):
        if not statusEffect.isCharacterAlreadyAffectedByStatus(target):
            target.status.append(statusEffect)
            print("{} is now affected by {}.".format(target.fullName, statusEffect.name))
        elif statusEffect.stackingEffect:
            currentStatusList = [currentStatus for currentStatus in target.status if
                                 currentStatus.name == statusEffect.name]
            currentStatusList[0].stackEffect(target)
            print("{}'s {} is aggravated.".format(target.fullName, statusEffect.name))
        else:
            targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
            print("But the {} had no effect on {}.".format(self.name, targetName))
        time.sleep(1)


class PlagueBomb(StatusInflictingItems):
    def __init__(self):
        super().__init__()
        self.name = "Plague Bomb"
        self.effect = "(Infects an enemy with poison)"
        self.status = [FFStatusSystem.Poison]
        self.itemAccuracy = 185


class DryGrassBomb(StatusInflictingItems):
    def __init__(self):
        super().__init__()
        self.name = "Dry Grass Bomb"
        self.effect = "(Infects an enemy with confusion)"
        self.status = [FFStatusSystem.Confusion]
        self.itemAccuracy = 175


class DryGrassSmoke(StatusInflictingItems):
    def __init__(self):
        super().__init__()
        self.targetQuantity = "All"
        self.name = "Dry Grass Smoke"
        self.effect = "(Infects all enemies with confusion)"
        self.status = [FFStatusSystem.Confusion]
        self.itemAccuracy = 145


class BitterWoodSap(StatusInflictingItems):
    def __init__(self):
        super().__init__()
        self.name = "Bitter Wood Sap"
        self.effect = "(Roots an enemy's body to the ground)"
        self.status = [FFStatusSystem.Root]
        self.itemAccuracy = 120


class ItemInstance:
    POTION = Potion()
    HIGH_POTION = HighPotion()
    PARTY_POTION = PartyPotion()
    ANTIDOTE = Antidote()
    SAGE_SALT = SageSalt()
    BRIGHT_HERB = BrightHerb()
    SOFT_SALVE = SoftSalve()
    PLAGUE_BOMB = PlagueBomb()
    DRY_GRASS_BOMB = DryGrassBomb()
    DRY_GRASS_SMOKE = DryGrassSmoke()
    BITTER_WOOD_SAP = BitterWoodSap()
