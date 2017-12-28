import time
import collections
import FFBattleSystem


class Inventory:
    def __init__(self):
        self.items = collections.OrderedDict()

    def checkInventory(self):
        for index, item, amount in enumerate(self.items.values()):
            print("\t\t{}. {}: {}  {}".format(index + 1, item.name, amount, item.effect))

    def addItem(self, item):
        if item in self.items.keys() and self.items[item] < 99:
            self.items[item] += 1
        elif item in self.items.keys():
            print("You cannot hold another {}.".format(item.name))
        else:
            self.items[item] = 1

    def removeItem(self, item):
        if self.items[item] < 1:
            self.items.pop(item)
        else:
            self.items[item] -= 1

    def useItem(self, allTargets):
        if not self.items:
            print("Your inventory is empty.")
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


class Item:
    def __init__(self, name):
        self.name = name
        self.effect = ""
        self.targetParty = "Enemy"
        self.targetQuantity = "All"
        self.power = 0
        self.removeStatus = []

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
                    targetAffiliation = "the enemies"
                else:
                    targetAffiliation = "your party"
                print("Use the {} on {}?".format(self.name, targetAffiliation))
                print("\t\t1. Yes")
                print("\t\t2. No")
                useItemBoolean = input()
                if useItemBoolean.lower() == "y":
                    self.resolveItem(targetList)
                    return True
                elif useItemBoolean.lower() == "n":
                    return False
                else:
                    print("That is not a valid response.")
            time.sleep(1)

    def resolveItem(self, target):
        pass
