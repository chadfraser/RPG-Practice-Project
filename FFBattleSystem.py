import random
import time
import collections
import FFSpellSystem


class Character:
    orderedSpellList = [FFSpellSystem.SpellInstance.CURE, FFSpellSystem.SpellInstance.FOG,
                        FFSpellSystem.SpellInstance.SANCTUARY, FFSpellSystem.SpellInstance.FIRE,
                        FFSpellSystem.SpellInstance.POISON_GAS, FFSpellSystem.SpellInstance.SLOW,
                        FFSpellSystem.SpellInstance.HASTE, FFSpellSystem.SpellInstance.STUN,
                        FFSpellSystem.SpellInstance.SOFT, FFSpellSystem.SpellInstance.CURSE,
                        FFSpellSystem.SpellInstance.DOOM, FFSpellSystem.SpellInstance.BANE]

    def __init__(self):
        self.name = ""
        self.fullName = self.name
        self.maxHP = 0
        self.currentHP = 0
        self.damage = 0
        self.defense = 0
        self.magicDef = 0
        self.evasion = 0
        self.accuracy = 0
        self.agility = 0
        self.criticalChance = 0
        self.strikeCount = 1

        self.weakness = []
        self.resistance = []
        self.spellsKnown = collections.OrderedDict()
        self.status = []

    # Controls the logic and flow of a character's physical attack
    def attackTarget(self, target):
        timesAttackDone = 0
        # A character attacks once for each strikeCount they have
        while timesAttackDone < self.strikeCount:
            # Checks if each attack hit the target
            if self.shouldAttackHit(target):
                # Runs the applyDamage function to determine the damage dealt by each successful attack
                damage, wasCritical = self.determineDamage(target)
                target.applyDamage(damage, wasCritical)
                # If the target becomes incapacitated, print a death message and don't apply any more attacks
                if target.isIncapacitated():
                    target.printDeathMessage()
                    break
            # Print a message upon the character missing the target
            else:
                self.printAttackMiss()
            timesAttackDone += 1

    # Determines whether the attacker hits their target for each strike
    def shouldAttackHit(self, target):
        # baseChanceToHit can be altered to fit new statuses as they are coded in (e.g., decreased by blindness)
        baseChanceToHit = 168
        # The attacking combatant will randomly hit or miss, based on the target's evasion and the attacker's accuracy
        toHitFormula = baseChanceToHit + self.accuracy - target.evasion
        randomCheckToHit = random.randint(1, 200)
        if randomCheckToHit <= toHitFormula:
            return True
        return False

    # Determines whether the attack should be a critical hit
    def shouldCriticalHit(self):
        criticalHitDiceRoll = random.randint(1, 200)
        # Attacks will randomly be critical hits, based on the attacker's critical chance
        if criticalHitDiceRoll <= self.criticalChance:
            return True
        return False

    # Determines how much damage an attack should do to the target
    def determineDamage(self, target):
        # Damage is a random number influenced by the attacker's damage score and the target's defense score
        penetratedDamage = random.randint(self.damage - target.defense, (2 * self.damage) - target.defense)
        # Damage has a minimum value of 1
        damage = max(1, penetratedDamage)
        wasCritical = self.shouldCriticalHit()
        if wasCritical:
            # Critical hits do additional damage that bypasses defense
            damage += random.randint(self.damage, 2 * self.damage)
        return damage, wasCritical

    # Decreases the target's HP after calculating damage from an attack
    def applyDamage(self, damage, wasCritical=False):
        self.currentHP -= damage
        self.printDamageAndCritical(damage, wasCritical)
        # HP has a minimum value of 0
        if self.currentHP <= 0:
            self.currentHP = 0
        # If the target was a hero, displays their current HP
        if isinstance(self, Hero):
            self.printCurrentHP()

    # Tests if a character is unable to act (e.g., if they are dead, frozen, turned to stone...)
    def isIncapacitated(self):
        if self.currentHP <= 0:
            return True
        return False

    # Tests if a character is weak to a particular element
    def isWeakToElement(self, element):
        return element in self.weakness

    # Tests if a character is resistant to a particular element
    def isResistantToElement(self, element):
        return element in self.resistance

    # Prints the damage dealt, and if the attack was a critical hit
    def printDamageAndCritical(self, damage, wasCritical):
        if wasCritical:
            print("--Critical hit!")
            time.sleep(1)
        print("--{} takes {} damage.".format(self.fullName, damage))
        time.sleep(1)

    # Prints the character's current HP
    def printCurrentHP(self):
        print("--{}'s HP is now {}.".format(self.fullName, self.currentHP))
        time.sleep(1)

    # Prints that the target was killed
    def printDeathMessage(self):
        print("--{} has fallen.".format(self.fullName))
        time.sleep(1)

    # Prints that the attacker missed
    def printAttackMiss(self):
        print("--{} missed!".format(self.fullName))
        time.sleep(1)

    # Prints the amount of HP that a character heals
    def printAmountHealed(self, healHPValue):
        print("--{} healed {} HP!".format(self.fullName, healHPValue))
        time.sleep(1)

    # Prints that a character's stat has increased
    def printStatBuffMessage(self, buffedStat):
        print("--{}'s {} has increased!".format(self.fullName, buffedStat.lower()))
        time.sleep(1)

    # Prints that a character's stat has decreased
    def printStatDebuffMessage(self, debuffedStat):
        print("--{}'s {} has gone down!".format(self.fullName, debuffedStat.lower()))
        time.sleep(1)

    # Controls the logic for the Paralysis status effect
    def controlParalysisStatusLogic(self):
        # If the character has Paralysis in their status list, generate a random number from 1 to 4 and return True
        if "Paralysis" in self.status:
            paralysisCheck = random.randint(1, 4)
            # The character is healed of Paralysis 25% of the time
            if paralysisCheck == 1:
                self.status.remove("Paralysis")
            return True
        return False

    # Heals the character a specific amount
    def healCharacter(self, healHPValue):
        self.currentHP = min(self.maxHP, self.currentHP + healHPValue)

    # Increases a particular stat of the character by a specific amount
    def buffCharacter(self, statusToBuff, statValue):
        if statusToBuff == "Defense":
            self.defense += statValue
            time.sleep(1)
        elif statusToBuff == "Strike Count":
            self.strikeCount += statValue
            time.sleep(1)

    # Decreases a particular stat of the character by a specific amount
    def debuffCharacter(self, statusToDebuff, statValue):
        if statusToDebuff == "Defense":
            self.defense = max(0, self.defense - statValue)
            time.sleep(1)
        elif statusToDebuff == "Strike Count":
            self.strikeCount = max(1, self.strikeCount - statValue)
            time.sleep(1)

    # Returns a list of strings containing the spells a character knows and how many charges of that spell remain
    def getListOfKnownSpellsAndCharges(self):
        tempList = list(self.spellsKnown.items())
        for spell, charges in tempList:
            tempList[tempList.index((spell, charges))] = ["{} ({} charges remaining)".format(spell.name, charges)
                                                          if charges != 1 else "{} (1 charge"
                                                                               " remaining)".format(spell.name)]
        return tempList

    # Puts the spells that a character knows in the proper order, as defined by the orderedSpellList
    def reorderCharacterSpellDict(self):
        tempSpellsKnownDict = collections.OrderedDict((spell, self.spellsKnown[spell]) for spell in
                                                      self.orderedSpellList if spell in self.spellsKnown)
        self.spellsKnown = tempSpellsKnownDict.copy()


class Hero(Character):
    def __init__(self):
        Character.__init__(self)
        self.currentHP = self.maxHP
        self.strength = 0
        self.damage = max(1, self.strength // 2)
        self.armor = 0
        self.defense = self.armor
        self.agility = 0
        self.evasion = self.agility
        self.intelligence = 0
        self.vitality = 0
        self.luck = 0
        self.hitRate = 0
        self.strikeCount = 1 + self.hitRate // 32
        self.accuracy = self.hitRate
        self.level = 1

    # Determines whether the hero successfully runs
    def shouldRun(self, listOfEnemies):
        # The chance of running is based on the enemy with the highest agility, and the acting hero's agility
        listOfEnemyAgility = [enemy.agility for enemy in listOfEnemies]
        maxEnemyAgility = max(listOfEnemyAgility)
        # If the enemy has over 200 agility, they are flagged as a boss, and thus cannot be run away from
        if maxEnemyAgility > 200:
            return False
        # Take a random number from 0 to twice the agility of the fastest enemy
        # If this number is lower than the acting hero's agility, the team successfully runs away
        randomCheckToRun = random.randint(0, 2 * maxEnemyAgility)
        if self.agility > randomCheckToRun:
            return True
        return False


# Represents a 'Fighter' type hero
class Fighter(Hero):
    def __repr__(self):
        return "Fighter"

    def __init__(self, name="FHTR"):
        super().__init__()
        self.maxHP = 73
        self.strength = 32
        self.armor = 15
        self.agility = 6
        self.intelligence = 2
        self.vitality = 10
        self.luck = 5
        self.hitRate = 24
        self.magicDef = 31
        self.criticalChance = 10
        self.name = name


# Represents a 'Thief' type hero
class Thief(Hero):
    def __repr__(self):
        return "Thief"

    def __init__(self, name="THEF"):
        super().__init__()
        self.maxHP = 59
        self.strength = 18
        self.armor = 5
        self.agility = 12
        self.intelligence = 6
        self.vitality = 6
        self.luck = 20
        self.hitRate = 21
        self.magicDef = 31
        self.criticalChance = 40
        self.name = name


# Represents a 'Monk' type hero
class Monk(Hero):
    def __repr__(self):
        return "Monk"

    def __init__(self, name="MONK"):
        super().__init__()
        self.maxHP = 68
        self.strength = 16
        self.armor = 8
        self.agility = 7
        self.intelligence = 6
        self.vitality = 23
        self.luck = 9
        self.hitRate = 14
        self.magicDef = 23
        self.criticalChance = 8
        self.strikeCount = 2 * max(1, 1 + self.hitRate // 32)
        self.name = name


# Represents a 'Red Mage' type hero
class RedMage(Hero):
    def __repr__(self):
        return "Red Mage"

    def __init__(self, name="RdMG"):
        super().__init__()
        self.maxHP = 54
        self.strength = 21
        self.armor = 15
        self.agility = 6
        self.intelligence = 11
        self.vitality = 8
        self.luck = 9
        self.hitRate = 16
        self.magicDef = 44
        self.criticalChance = 10
        self.spellsKnown = collections.OrderedDict([(FFSpellSystem.SpellInstance.CURE, 2),
                                                    (FFSpellSystem.SpellInstance.FIRE, 2)])
        self.name = name


# Represents a 'White Mage' type hero
class WhiteMage(Hero):
    def __repr__(self):
        return "White Mage"

    def __init__(self, name="WhMG"):
        super().__init__()
        self.maxHP = 56
        self.strength = 14
        self.armor = 3
        self.agility = 12
        self.intelligence = 18
        self.vitality = 11
        self.luck = 11
        self.hitRate = 8
        self.magicDef = 44
        self.criticalChance = 5
        self.spellsKnown = collections.OrderedDict([(FFSpellSystem.SpellInstance.CURE, 3),
                                                    (FFSpellSystem.SpellInstance.FOG, 2),
                                                    (FFSpellSystem.SpellInstance.SANCTUARY, 2)])
        self.name = name


# Represents a 'Black Mage' type hero
class BlackMage(Hero):
    def __repr__(self):
        return "Black Mage"

    def __init__(self, name="BlMG"):
        super().__init__()
        self.maxHP = 47
        self.strength = 11
        self.armor = 3
        self.agility = 11
        self.intelligence = 23
        self.vitality = 2
        self.luck = 14
        self.hitRate = 18
        self.magicDef = 44
        self.criticalChance = 15
        self.spellsKnown = collections.OrderedDict([(FFSpellSystem.SpellInstance.FIRE, 3),
                                                    (FFSpellSystem.SpellInstance.POISON_GAS, 2),
                                                    (FFSpellSystem.SpellInstance.SLOW, 2)])
        self.name = name


class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
        self.fullName = "Enemy " + self.name
        self.currentHP = self.maxHP
        self.contactStatus = ''
        self.spellChance = 0


# Represents a 'Goblin' type enemy
class Goblin(Enemy):
    def __repr__(self):
        return "Goblin"

    def __init__(self, name="Goblin"):
        super().__init__()
        self.maxHP = 18
        self.damage = 8
        self.defense = 3
        self.evasion = 6
        self.accuracy = 8
        self.agility = 18
        self.magicDef = 16
        self.criticalChance = 4
        self.name = name


# TO BE IMPLEMENTED LATER
# class StatusEffect:
#     def __init__(self, name):
#         self.name = name
#         self.endsAfterBattle = True
#
#     def isIncapacitated(self):
#         if self.name in ["Stone"]:
#             return True
#         return False
#
#     def cannotAct(self):
#         if self.name in ["Paralysis", "Sleep"]:
#             return True
#         return False
#
#     def applyStatusDamage(self, character):
#         pass
#
#     # Prints that a character has died from the Doom status
#     def printDoomMessage(self, character):
#         print("--{}'s lifeline has been cut short by dark magic.".format(character.fullName))
#         time.sleep(1)
#         character.printDeathMessage()
#
#     # Controls the logic for the Doom status effect
#     def controlDoomStatusLogic(self, character):
#         # If the character has Doom in their status list, remove it from the list
#         sublist = isInList(character.status, "Doom")
#         if sublist:
#             sublist.remove("Doom")
#             # If that was the last copy of Doom in their status list, that character dies and a message prints
#             if "Doom" not in sublist:
#                 character.currentHP = 0
#                 character.printDoomMessage()
#
#
# class ParalysisStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class PoisonStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class StoneStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class BlindStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class MuteStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class SleepStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class ConfusionStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class DoomStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()
#
#
# class HolyStatus(StatusEffect):
#     def __init__(self):
#         super().__init__()


####################################
####################################
####################################


# CURRENTLY NOT USED: MAY BE USED IN FUTURE
# def isInList(listOfLists, searchedQuery):
#     for specificList in listOfLists:
#         if searchedQuery in specificList:
#             return specificList


# Allows the player to choose the target of an attack, spell, item, etc.
def chooseTarget(targetList):
    # Loops until the player chooses a legal target
    while True:
        print("Choose your target.")
        time.sleep(1)
        # Prints all available targets, and the indices to each available target
        for index, target in enumerate(targetList):
            print("\t\t{}. {}".format(index + 1, target))
        print("\t\tc. Cancel")
        targetChosen = input()
        # Returns the chosen index, or None if the player chose to cancel the action
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(targetList):
            return int(targetChosen)
        elif targetChosen == "c".lower():
            return None
        print("That is not a valid response.")
        time.sleep(1)


def chooseSpell(actingHero, targetList):
    # Loops until the player chooses a legal target
    while True:
        print("Choose which spell you'd like to cast.")
        time.sleep(1)
        # Prints all available targets, and the indices to each available target
        for index, target in enumerate(targetList):
            print("\t\t{}. {}".format(index + 1, target[0]))
        print("\t\tc. Cancel")
        targetChosen = input()
        # Returns the chosen index, or None if the player chose to cancel the action
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(targetList):
            spellChosen = list(actingHero.spellsKnown.keys())[int(targetChosen) - 1]
            if actingHero.spellsKnown[spellChosen] > 0:
                return int(targetChosen)
            print("You cannot cast that spell anymore.")
            time.sleep(1)
        elif targetChosen == "c".lower():
            return None
        else:
            print("That is not a valid response.")
            time.sleep(1)


# Takes a list of all enemies and heroes in the fight and returns a shuffled copy of that list
# Used for randomly determining who acts in what order in combat
def determineInitiative(combatantList):
    clonedInitiativeList = combatantList[:]
    random.shuffle(clonedInitiativeList)
    return clonedInitiativeList


# Prints the current round of combat and all surviving combatants on either side
def printCurrentRoundDetails(currentRound, heroList, enemyList):
    # Displays the current round
    print("\n\tROUND {}!".format(currentRound))
    time.sleep(2)
    # Displays all surviving combatants, putting a comma between them
    print(', '.join(str(combatant.name) for combatant in heroList))
    print("\t\tVS\n\t", end='')
    print(', '.join(str(combatant.name) for combatant in enemyList) + "\n")
    time.sleep(2)


def chooseTurnAction(actingHero, livingHeroes, livingEnemies):
    listOfOptions = ["Attack", "Cast a spell", "Use an item", "Run away"]
    while True:
        print("{}! Choose your action.".format(actingHero.name))
        time.sleep(0.5)
        # Prints all available targets, and the indices to each available target
        for index, option in enumerate(listOfOptions):
            print("\t\t{}. {}".format(index + 1, option))
        targetChosen = input()
        # Returns the chosen index, or None if the player chose to cancel the action
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(listOfOptions):
            actionChosenBoolean = controlActionChoiceLogic(actingHero, livingHeroes, livingEnemies,
                                                           int(targetChosen))
            if actionChosenBoolean:
                break
        else:
            print("That is not a valid response.")
            time.sleep(1)


def controlActionChoiceLogic(actingHero, livingHeroes, livingEnemies, actionChosen):
    # If the hero chooses to physically attack
    if actionChosen == 1:
        targetChosen = chooseTarget(livingEnemies)
        if targetChosen:
            print("{} attacks enemy {}!".format(actingHero.name, livingEnemies[targetChosen - 1].name))
            time.sleep(1.5)
            actingHero.attackTarget(livingEnemies[targetChosen - 1])
            return True
    # If the hero chooses to cast a spell
    elif actionChosen == 2:
        actingHero.reorderCharacterSpellDict()
        spellListWithCharges = actingHero.getListOfKnownSpellsAndCharges()
        if not actingHero.spellsKnown or all(value == 0 for value in actingHero.spellsKnown.values()):
            print("You cannot cast a spell now.")
            time.sleep(1.5)
            return False
        spellChosen = chooseSpell(actingHero, spellListWithCharges)
        if spellChosen:
            livingCombatants = livingHeroes + livingEnemies
            spellCastBoolean = FFSpellSystem.Spell.castSpellSuperclassMethod(spellChosen - 1, actingHero,
                                                                             livingCombatants)
            if spellCastBoolean:
                return True
    # If the hero chooses to use an item
    elif actionChosen == 3:
        pass  # Define item use
    # If the hero chooses to run
    elif actionChosen == 4:
        if actingHero.shouldRun(livingEnemies):
            for enemy in livingEnemies:
                enemy.currentHP = 0
            print("Escaped!")
        else:
            print("You couldn't escape!")
        time.sleep(1.5)
        return True
    return False


# Controls the flow of combat between heroes and enemies
def controlCombatSystemLogic(heroList, enemyList):
    listOfCombatants = (heroList + enemyList)
    battleInProgress = True
    roundCount = 0
    for enemy in enemyList:
        enemy.currentHP = enemy.maxHP
        enemy.fullName = "Enemy " + enemy.name
    livingEnemies = [enemy for enemy in enemyList if enemy.currentHP > 0]
    livingHeroes = [hero for hero in heroList if hero.currentHP > 0]
    while battleInProgress:
        roundCount += 1
        # Each round, randomizes the order in which combatants act
        currentRoundInitiative = determineInitiative(listOfCombatants)
        # Prints the current round of combat and all surviving combatants on either side
        printCurrentRoundDetails(roundCount, livingHeroes, livingEnemies)
        for turnOrder in range(len(listOfCombatants)):
            currentActingCombatant = currentRoundInitiative[turnOrder]
            # If the current attacker is a hero and there are surviving enemies, they are given a list of all
            # surviving enemies, and choose which one to attack
            if currentActingCombatant in livingHeroes and len(livingEnemies) > 0:
                chooseTurnAction(currentActingCombatant, livingHeroes, livingEnemies)
                # If the hero chooses to physically attack
            # If the current attacker is an enemy and there are surviving heroes, they randomly attack one
            elif currentActingCombatant in livingEnemies and len(livingHeroes) > 0:
                targetChosen = random.randint(0, len(livingHeroes) - 1)
                print("{} attacks {}!".format(currentActingCombatant.fullName, livingHeroes[targetChosen - 1].name))
                time.sleep(1.5)
            livingEnemies = [enemy for enemy in enemyList if enemy.currentHP > 0]
            livingHeroes = [hero for hero in heroList if hero.currentHP > 0]
            # The battle ends once one side is completely defeated
            if livingHeroes == [] or livingEnemies == []:
                battleInProgress = False

#
# # if __name__ == '__main__':  # del
# #    main()  # del
#

