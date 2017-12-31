import random
import time
import FFBattleSystem


class StatusEffect:
    def __init__(self):
        self.name = ""
        self.canAct = True
        self.curedAfterBattle = False
        self.effectOutsideOfBattle = False
        self.effectUponCure = False
        self.stackingEffect = False
        self.isIncapacitated = False

    @classmethod
    def createNewStatusInstance(cls):
        return cls

    def isCharacterAlreadyAffectedByStatus(self, target):
        statusList = [statusEffect for statusEffect in target.status if statusEffect.name != self.name]
        if statusList == target.status and target.currentHP > 0:
            self.effectOnStatus(target)
            return False
        return True

    def cureStatusEffect(self, target):
        statusList = [statusEffect for statusEffect in target.status if statusEffect.name != self.name]
        target.status = statusList
        self.effectOnCure(target)

    def activateStatus(self, target):
        pass

    def startOfTurnEffect(self, target):
        pass

    def effectOnStatus(self, target):
        pass

    def effectOnCure(self, target):
        pass


class Unconscious(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Unconscious"
        self.canAct = False
        self.isIncapacitated = True

    def activateStatus(self, target):
        if target.currentHP > 0:
            self.cureStatusEffect(target)


class Paralysis(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Paralysis"
        self.canAct = False
        self.curedAfterBattle = True

    def activateStatus(self, target):
        pass

    def startOfTurnEffect(self, target):
        paralysisCheck = random.randint(1, 4)
        if paralysisCheck == 1:
            print("{}'s body stops shaking!".format(target.fullName))
            target.status.remove(self)
            time.sleep(1)
            return True
        else:
            print("{} is still paralyzed!".format(target.fullName))
            time.sleep(1)
            return False


class Sleep(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Sleep"
        self.canAct = False
        self.curedAfterBattle = True

    def activateStatus(self, target):
        pass

    def startOfTurnEffect(self, target):
        sleepCheck = random.randint(1, 200)
        if sleepCheck <= target.currentHP:
            print("{} wakes up!".format(target.fullName))
            target.status.remove(self)
            time.sleep(1)
            return True
        else:
            print("{} is asleep!".format(target.fullName))
            time.sleep(1)
            return False


class Confusion(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Confusion"
        self.curedAfterBattle = True

    def activateStatus(self, target):
        pass

    def startOfTurnEffect(self, target):
        confusionCheck = random.randint(1, 8)
        if confusionCheck == 1:
            print("{} is no longer confused!".format(target.fullName))
            target.status.remove(self)
            time.sleep(1)
        else:
            print("{} is still confused!".format(target.fullName))
            time.sleep(1)
            return True


class Blind(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Blind"
        self.curedAfterBattle = True
        self.effectUponCure = True

    def effectOnStatus(self, target):
        target.evasion = int(target.evasion * 1 // 4)
        target.accuracy = int(target.accuracy * 3 // 4)

    def effectOnCure(self, target):
        target.evasion = int(target.evasion * 4)
        target.accuracy = int(target.accuracy * 4 // 3)


class Silence(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Silence"
        self.curedAfterBattle = True

    def activateStatus(self, target):
        pass


class Poison(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Poison"
        self.effectOutsideOfBattle = True
        self.stackingEffect = True
        self.poisonCount = 1

    # Controls the logic for the Paralysis status effect
    def startOfTurnEffect(self, target):
        poisonDamage = 2 ** self.poisonCount
        target.currentHP -= poisonDamage
        print("{} suffers {} damage from poison.".format(target.fullName, poisonDamage))
        time.sleep(1)
        if target.currentHP <= 0:
            target.currentHP = 0
            target.printDeathMessage()

    def stackEffect(self, target):
        self.poisonCount += 1

    def effectOutsideOfBattle(self, target):
        target.currentHP -= 2
        if target.currentHP <= 0:
            target.currentHP = 0
            target.printDeathMessage()


class Holy(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Holy"
        self.curedAfterBattle = True
        self.stackingEffect = True
        self.holyTurnCount = 5
        self.holyHPCount = 1

    def startOfTurnEffect(self, target):
        holyHPValue = 2 ** self.holyHPCount
        target.printAmountHealed(holyHPValue)
        target.healCharacter(holyHPValue)
        if isinstance(target, FFBattleSystem.Hero):
            target.printCurrentHP()
        self.holyTurnCount -= 1
        if self.holyTurnCount == 0:
            target.status.remove(self)

    def stackEffect(self, target):
        self.holyHPCount += 2


class Stone(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Stone"
        self.canAct = False
        self.isIncapacitated = True


class Root(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Root"
        self.canAct = False
        self.isIncapacitated = True


class Doom(StatusEffect):
    def __init__(self):
        super().__init__()
        self.name = "Doom"
        self.curedAfterBattle = True
        self.stackingEffect = True
        self.doomCount = 3

    def startOfTurnEffect(self, target):
        if self.doomCount == 0:
            target.status.remove(self)
            target.currentHP = 0
            print("--{}'s lifeline has been cut short by dark magic.".format(target.fullName))
            target.status = [Unconscious()]
            time.sleep(1)
            target.printDeathMessage()
        else:
            self.doomCount -= 1

    def stackEffect(self, target):
        self.doomCount = max(0, self.doomCount - 1)
