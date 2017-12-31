import random
import time
import collections
import FFSpellSystem
import FFItemSystem
import FFStatusSystem

playerCurrentInventory = FFItemSystem.Inventory()


class Character:
    orderedSpellList = [FFSpellSystem.SpellInstance.CURE, FFSpellSystem.SpellInstance.FOG,
                        FFSpellSystem.SpellInstance.SANCTUARY, FFSpellSystem.SpellInstance.FIRE,
                        FFSpellSystem.SpellInstance.POISON_SMOKE, FFSpellSystem.SpellInstance.SLOW,
                        FFSpellSystem.SpellInstance.BEACON, FFSpellSystem.SpellInstance.SILENCE,
                        FFSpellSystem.SpellInstance.HASTE, FFSpellSystem.SpellInstance.STUN,
                        FFSpellSystem.SpellInstance.SOFT, FFSpellSystem.SpellInstance.CURSE,
                        FFSpellSystem.SpellInstance.DOOM, FFSpellSystem.SpellInstance.BANE,
                        FFSpellSystem.SpellInstance.PURGE,
                        FFSpellSystem.SpellInstance.ARMAGEDDON, FFSpellSystem.SpellInstance.JUDGMENT]

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
        self.equipment = []
        self.experience = 0

    def activateStartOfTurnStatusEffects(self):
        tempStatusList = self.status[:]
        for statusEffect in tempStatusList:
            statusEffect.startOfTurnEffect(self)
            if self.currentHP == 0:
                break

    def attackTargetWithoutControl(self, targetList):
        targetChosen = random.randint(0, len(targetList) - 1)
        print("{} attacks without thinking.".format(self.fullName))
        time.sleep(1)
        self.attackTarget(targetList[targetChosen])
        time.sleep(1.5)

    # Controls the logic and flow of a character's physical attack
    def attackTarget(self, target):
        timesAttackDone = 0
        self.printAttackTarget(target)
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
            self.status = [FFStatusSystem.Unconscious()]
        # If the target was a hero, displays their current HP
        if isinstance(self, Hero):
            self.printCurrentHP()

    # Tests if a character is unable to act (e.g., if they are dead, frozen, turned to stone...)
    def isIncapacitated(self):
        if self.currentHP <= 0:
            return True
        for statusEffect in self.status:
            if statusEffect.isIncapacitated:
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

    def printAttackTarget(self, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        if self == target:
            print("{} attacks themselves!".format(self.fullName))
        else:
            print("{} attacks {}!".format(self.fullName, targetName))
        time.sleep(1.5)

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

    # Heals the character a specific amount
    def healCharacter(self, healHPValue):
        self.currentHP = min(self.maxHP, self.currentHP + healHPValue)

    # Increases a particular stat of the character by a specific amount
    def buffCharacter(self, statToBuff, statValue):
        if statToBuff == "Defense":
            self.defense += statValue
            time.sleep(1)
        elif statToBuff == "Strike Count":
            self.strikeCount += statValue
            time.sleep(1)
        elif statToBuff == "Evasion":
            self.evasion += statValue
            time.sleep(1)

    # Decreases a particular stat of the character by a specific amount
    def debuffCharacter(self, statToDebuff, statValue):
        if statToDebuff == "Defense":
            self.defense = max(0, self.defense - statValue)
            time.sleep(1)
        elif statToDebuff == "Strike Count":
            self.strikeCount = max(1, self.strikeCount - statValue)
            time.sleep(1)
        elif statToDebuff == "Evasion":
            self.strikeCount = max(0, self.evasion - statValue)
            time.sleep(1)


class Hero(Character):
    playerStartingParty = []

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

    def setHeroDefaultValues(self):
        self.damage = max(1, self.strength // 2)
        self.defense = self.armor
        self.evasion = self.agility
        self.strikeCount = 1 + self.hitRate // 32
        self.accuracy = self.hitRate
        self.fullName = self.name

    # Returns a list of strings containing the spells a character knows and how many charges of that spell remain
    def getListOfKnownSpellsAndCharges(self):
        tempList = list(self.spellsKnown.items())
        print()
        for spell, charges in tempList:
            tempList[tempList.index((spell, charges))] = ["{} ({} charges remaining)".format(spell.name, charges[0])
                                                          if charges != 1 else "{} (1 charge"
                                                                               " remaining)".format(spell.name)]
        return tempList

    # Puts the spells that a character knows in the proper order, as defined by the orderedSpellList
    def reorderCharacterSpellDict(self):
        tempSpellsKnownDict = collections.OrderedDict((spell, self.spellsKnown[spell]) for spell in
                                                      self.orderedSpellList if spell in self.spellsKnown)
        self.spellsKnown = tempSpellsKnownDict.copy()

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

    # Shows the player all of the hero's known spells, and lets them choose which spell to cast
    def selectAndCastSpell(self, livingHeroes, livingEnemies):
        # Properly orders the hero's spell dictionary
        self.reorderCharacterSpellDict()
        # Gets a list of strings of the spell dictionary's values, and how many charges of each of those spells remain
        spellListWithCharges = self.getListOfKnownSpellsAndCharges()
        # Immediately cancel the action if the hero does not have any spell charges
        if not self.spellsKnown or all(value[0] == 0 for value in self.spellsKnown.values()):
            print("You cannot cast a spell now.")
            time.sleep(1.5)
            return False
        # Otherwise, let the hero choose which spell they wish to cast
        spellChosen = chooseSpell(self, spellListWithCharges)
        # If the hero does not cancel the action, pass the chosen spell to the FFSpellSystem module so it can run the
        # logic on casting the spell
        if spellChosen:
            livingCombatants = livingHeroes + livingEnemies
            spellCastCompleted = FFSpellSystem.Spell.castSpellSuperclassMethod(spellChosen - 1, self, livingCombatants)
            # Return True if the hero did not cancel the action at any point, or False if they did
            if spellCastCompleted:
                return True
        return False


# Represents a 'Fighter' type hero
class Fighter(Hero):
    def __str__(self):
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
    def __str__(self):
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
    def __str__(self):
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
    def __str__(self):
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
        self.spellsKnown = collections.OrderedDict([(FFSpellSystem.SpellInstance.CURE, [2, 2]),
                                                    (FFSpellSystem.SpellInstance.FIRE, [2, 2])])
        self.name = name


# Represents a 'White Mage' type hero
class WhiteMage(Hero):
    def __str__(self):
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
        self.spellsKnown = collections.OrderedDict([(FFSpellSystem.SpellInstance.CURE, [3, 3]),
                                                    (FFSpellSystem.SpellInstance.FOG, [2, 2]),
                                                    (FFSpellSystem.SpellInstance.SANCTUARY, [2, 2])])
        self.name = name


# Represents a 'Black Mage' type hero
class BlackMage(Hero):
    def __str__(self):
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
        self.spellsKnown = collections.OrderedDict([(FFSpellSystem.SpellInstance.FIRE, [3, 3]),
                                                    (FFSpellSystem.SpellInstance.POISON_SMOKE, [2, 2]),
                                                    (FFSpellSystem.SpellInstance.SLOW, [2, 2])])
        self.name = name


class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
        self.fullName = "Enemy " + self.name
        self.currentHP = self.maxHP
        self.contactStatus = []
        self.spellChance = 0

    def setEnemyDefaultValues(self):
        self.currentHP = self.maxHP
        self.fullName = "Enemy " + self.name


# Represents a 'Goblin' type enemy
class Goblin(Enemy):
    def __str__(self):
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
        self.experience = 6
        self.name = name


####################################
####################################
####################################


# CURRENTLY NOT USED: MAY BE USED IN FUTURE
# def isInList(listOfLists, searchedQuery):
#     for specificList in listOfLists:
#         if searchedQuery in specificList:
#             return specificList


# Allows the player to choose the target of an attack, item, etc.
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
        elif targetChosen.lower() == "c":
            return None
        print("That is not a valid response.")
        time.sleep(1)


# Allows the player to choose the spell they wish to cast
def chooseSpell(actingHero, spellList):
    # Loops until the player chooses a legal target
    while True:
        print("Choose which spell you'd like to cast.")
        time.sleep(1)
        # Prints all available targets, and the indices to each available target
        for index, target in enumerate(spellList):
            print("\t\t{}. {}".format(index + 1, target[0]))
        print("\t\tc. Cancel")
        targetChosen = input()
        # Returns the chosen index, or None if the player chose to cancel the action
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(spellList):
            spellChosen = list(actingHero.spellsKnown.keys())[int(targetChosen) - 1]
            if actingHero.spellsKnown[spellChosen][0] > 0:
                return int(targetChosen)
            print("You cannot cast that spell anymore.")
            time.sleep(1)
        elif targetChosen.lower() == "c":
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


# Takes player input to determine which action they'd like to do that turn
def chooseTurnAction(actingHero, livingHeroes, livingEnemies):
    listOfOptions = ["Attack", "Cast a spell", "Use an item", "Run away", "Examine party"]
    while True:
        print("{}! Choose your action.".format(actingHero.name))
        time.sleep(0.5)
        # Prints all available targets, and the indices to each available target
        for index, option in enumerate(listOfOptions):
            print("\t\t{}. {}".format(index + 1, option))
        targetChosen = input()
        # Passes the chosen index to a function that determines which function to use it in
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(listOfOptions):
            wasActionCompleted = applyTurnAction(actingHero, livingHeroes, livingEnemies, int(targetChosen))
            # If the player did not cancel the function, break out of the loop to end their turn
            if wasActionCompleted:
                break
        else:
            print("That is not a valid response.")
            time.sleep(1)


# Determines which functions to call, depending on which action the player chose
def applyTurnAction(actingHero, livingHeroes, livingEnemies, actionChosen):
    actionCompleted = False
    if actionChosen == 1:
        actionCompleted = False
        targetChosen = chooseTarget(livingEnemies)
        if targetChosen:
            actingHero.attackTarget(livingEnemies[targetChosen - 1])
            actionCompleted = True
    elif actionChosen == 2:
        if any(statusEffect.name == "Silence" for statusEffect in actingHero.status):
            print("{} is Silenced, and cannot cast magic.".format(actingHero.name))
            time.sleep(1)
            return False
        actionCompleted = actingHero.selectAndCastSpell(livingHeroes, livingEnemies)
    elif actionChosen == 3:
        actionCompleted = playerCurrentInventory.useItem(livingHeroes + livingEnemies)
    elif actionChosen == 4:
        actionCompleted = attemptToRun(actingHero, livingEnemies)
    # Note that this action always returns false, as examining the battlefield does not use up a turn
    elif actionChosen == 5:
        actionCompleted = examineBattlefield()
    # If the player did not cancel the action, return True so the chooseTurnAction function will break from its loop
    if actionCompleted:
        return True
    # If the player did cancel the action, return False so the chooseTurnAction function will loop
    return False


def attemptToRun(actingHero, livingEnemies):
    if actingHero.shouldRun(livingEnemies):
        for enemy in livingEnemies:
            enemy.currentHP = 0
        print("Escaped!")
    else:
        print("You couldn't escape!")
    time.sleep(1.5)
    return True


def examineBattlefield():
    for hero in Hero.playerStartingParty:
        print("{}'s HP: {} / {}".format(hero.name, hero.currentHP, hero.maxHP))
        heroStatusList = [statusEffect.name for statusEffect in hero.status]
        heroStatusString = ', '.join(heroStatusList)
        print("{}'s status: {}".format(hero.name, heroStatusString or 'Healthy'))
        time.sleep(0.5)
    time.sleep(1.5)
    print()
    return False


# Controls the flow of combat between heroes and enemies
def startCombat(heroList, enemyList):
    listOfCombatants = heroList + enemyList
    battleInProgress = True
    roundCount = 0
    # Set t
    for enemy in enemyList:
        enemy.setEnemyDefaultValues()
    for hero in heroList:
        hero.setHeroDefaultValues()
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
                currentActingCombatant.activateStartOfTurnStatusEffects()
                if all(statusEffect.canAct for statusEffect in currentActingCombatant.status):
                    if any(statusEffect.name == "Confusion" for statusEffect in currentActingCombatant.status):
                        currentActingCombatant.attackTargetWithoutControl(livingHeroes + livingEnemies)
                    else:
                        chooseTurnAction(currentActingCombatant, livingHeroes, livingEnemies)
                    time.sleep(1.5)
            # If the hero chooses to physically attack
            # If the current attacker is an enemy and there are surviving heroes, they randomly attack one
            elif currentActingCombatant in livingEnemies and len(livingHeroes) > 0:
                currentActingCombatant.activateStartOfTurnStatusEffects()
                if all(statusEffect.canAct for statusEffect in currentActingCombatant.status):
                    if any(statusEffect.name == "Confusion" for statusEffect in currentActingCombatant.status):
                        currentActingCombatant.attackTargetWithoutControl(livingHeroes + livingEnemies)
                    else:
                        targetChosen = random.randint(0, len(livingHeroes) - 1)
                        currentActingCombatant.attackTarget(livingHeroes[targetChosen])
                        time.sleep(1.5)
            livingEnemies = [enemy for enemy in enemyList if not enemy.isIncapacitated()]
            livingHeroes = [hero for hero in heroList if not hero.isIncapacitated()]
            # The battle ends once one side is completely defeated
            if livingHeroes == [] or livingEnemies == []:
                battleInProgress = False
