import random
import time


class Character:
    def __init__(self):
        self.name = ""
        self.maxHP = 0
        self.currentHP = 0
        self.damage = 0
        self.defense = 0
        self.magicDef = 0
        self.evasion = 0
        self.accuracy = 0
        self.criticalChance = 0
        self.hitAmount = 1

        self.weakness = []
        self.resistance = []
        self.spellsKnown = {}
        self.orderedSpellDictionary = ["Cure", "Fog", "Sanctuary", "Fire", "Poison Smoke", "Slow", "Stun", "Curse",
                                       "Hex"]
        self.status = []

    # Controls the logic and flow of a character's physical attack
    def controlAttackLogic(self, target):
        timesAttackDone = 0
        # A character attacks once for each hitAmount they have
        while timesAttackDone < self.hitAmount:
            if self.shouldAttackHit(target):
                # Runs the applyDamage function to determine the damage dealt by each successful attack
                self.applyDamage(target)
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
    def applyDamage(self, target):
        damage, wasCritical = self.determineDamage(target)
        target.currentHP -= damage
        target.printDamageAndCritical(damage, wasCritical)
        # HP has a minimum value of 0
        if target.currentHP <= 0:
            target.currentHP = 0
        # If the target was a hero, displays their current HP
        if isinstance(target, Hero):
            target.printCurrentHP()

    # Tests if a character is unable to act (e.g., if they are dead, frozen, turned to stone...)
    def isIncapacitated(self):
        if self.currentHP <= 0:
            return True
        return False

    # Prints the damage dealt, and if the attack was a critical hit
    def printDamageAndCritical(self, damage, wasCritical):
        if wasCritical:
            print("--Critical hit!")
            time.sleep(1)
        entityName = "Enemy " + self.name if isinstance(self, Enemy) else self.name
        print("--" + entityName + " takes " + str(damage) + " damage.")
        time.sleep(0.5)

    # Prints the character's current HP
    def printCurrentHP(self):
        entityName = "Enemy " + self.name if isinstance(self, Enemy) else self.name
        print("--" + entityName + "'s HP is now " + str(self.currentHP) + ".")
        time.sleep(0.3)

    # Prints that the target was killed
    def printDeathMessage(self):
        entityName = "Enemy " + self.name if isinstance(self, Enemy) else self.name
        print(entityName + " has fallen.")
        time.sleep(0.3)

    # Prints that the attacker missed
    def printAttackMiss(self):
        entityName = "Enemy " + self.name if isinstance(self, Enemy) else self.name
        print("--" + entityName + " missed!")
        time.sleep(0.3)

    def printAmountHealed(self, cureHPValue):
        print("--" + self.name + " healed " + str(cureHPValue) + " HP!")
        time.sleep(0.5)


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
        self.hitAmount = 1 + self.hitRate // 32
        self.accuracy = self.hitRate

    def chooseSpellToCast(self):
        # Loops until the hero chooses a legal target
        while True:
            print(self.name + "! Choose which spell to cast:")
            time.sleep(0.5)
            orderedSpellList = [spell for spell in self.orderedSpellDictionary if
                                spell in self.spellsKnown.keys() and not self.spellsKnown[len(orderedSpellList)] == 0]
            print("\t\tc. Cancel")
            spellSelectionChosen = input()
            # Recognizes the spell the hero chose to cast, or repeats the loop if the hero chose an invalid target
            if spellSelectionChosen.isnumeric() and 0 < int(spellSelectionChosen) <= len(self.spellsKnown):
                # Ensures that the enumerated choice corresponds to the proper spell in the orderedSpellDictionary
                if self.spellsKnown[int(spellSelectionChosen) - 1] > 0:
                    return int(spellSelectionChosen)
                else:
                    print("You cannot cast that spell now.")
                    time.sleep(1)
            # Tells the attack program to reiterate selecting an enemy if you cancel your spell
            elif spellSelectionChosen == "c".lower():
                return None
            else:
                print("That is not a valid response.")
                time.sleep(1)

    def castSpellLogic(self, heroList, enemyList):
        # Loops until the hero chooses a legal target
        tempSpellList = [spell for spell in self.orderedSpellDictionary if spell in self.spellsKnown.keys()]
        indexOfSpellChosen = self.chooseSpellToCast()
        spellChosen = tempSpellList[indexOfSpellChosen - 1]
        #  Tests if you have a charge remaining in that spell
        if indexOfSpellChosen:
            pass
        else:
            print("That is not a valid response.")
            time.sleep(1)


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
        self.luck = 7
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
        self.luck = 18
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
        self.luck = 7
        self.hitRate = 14
        self.magicDef = 23
        self.criticalChance = 8
        self.hitAmount = 2 * max(1, 1 + self.hitRate // 32)
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
        self.luck = 7
        self.hitRate = 16
        self.magicDef = 44
        self.criticalChance = 10
        self.spellsKnown = {"Cure": 2, "Fire": 2}
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
        self.luck = 7
        self.hitRate = 8
        self.magicDef = 44
        self.criticalChance = 5
        self.spellsKnown = {"Cure": 3, "Fog": 2, "Sanctuary": 2}
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
        self.luck = 11
        self.hitRate = 18
        self.magicDef = 44
        self.criticalChance = 15
        self.spellsKnown = {"Fire": 3, "Poison Smoke": 2, "Slow": 2}
        self.name = name


class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
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
        self.magicDef = 16
        self.criticalChance = 4
        self.name = name


class Spell:
    def __init__(self):
        self.target = None
        self.name = ""
        self.effect = ""

    def chooseSpellTarget(self, actingHero, targetList):
        # Loop reiterates until the player chooses a valid target
        while True:
            selectedTargetOfSpell = []
            print("Choose the target for your " + self.name + " spell " + self.effect)
            # If the spell only targets one character, prints an enumerated list of all possible targets
            if self.target == "One":
                for character in targetList:
                    print("\t\t" + str(targetList.index(character) + 1) + ". " + character.name)
            # If the spell targets all heroes, give the player only the option to select all heroes, or the
            # option to cancel
            elif self.target == "All":
                print("\t\t1. All heroes" if isinstance(targetList[0], Hero) else print("\t\t1. All enemies"))
            print("\t\tc. Cancel")
            targetInput = input()
            # Recognizes the player's input and relates it to the target
            if targetInput.isnumeric() and 0 <= int(targetInput) - 1 < len(targetList) and self.target == "One":
                selectedTargetOfSpell.append(targetList[int(targetInput) - 1])
                # Removes one charge of the spell being cast
                # Provides unique flavor text for the spell, ending with the target hero's name
                actingHero.spellsKnown[self.name] -= 1
                print(self.spellText + selectedTargetOfSpell[0].name + self.secondaryText, end='')
                return selectedTargetOfSpell
            elif targetInput == "1" and self.target == "All":
                selectedTargetOfSpell = [character for character in targetList]
                # Removes one charge of the spell being cast
                # Provides unique flavor text for the spell
                actingHero.spellsKnown[self.name] -= 1
                print(self.spellText, end='')
                return selectedTargetOfSpell
            # Returns to the attack selection phase if the player cancels the spell
            elif targetInput == "c".lower():
                return False
            else:
                print("That is not a valid response.")
                time.sleep(1)

    def shouldSpellHit(self, target):
        # The chance to hit can be modified as needed
        baseChanceToHit = 148
        if self.spellElement in target.resistance:
            baseChanceToHit = 0
        if self.spellElement in target.weakness:
            baseChanceToHit += 40
        # Targets resistant to the spell's element are very unlikely to be hit directly by the spell
        # Targets weak to the spell's element are more likely to be hit directly by the spell
        # Spell accuracy and the target's magic defense influence whether the spell hits directly or not
        spellToHit = baseChanceToHit + self.spellAccuracy - target.magicDef
        randomCheckToHit = random.randint(1, 200)
        if randomCheckToHit <= spellToHit:
            return True
        return False


class HealingSpell(Spell):
    def __init__(self):
        super().__init__()
        self.spellPower = 0

    # Controls the logic for all spells that heal the target's HP
    def controlHealingSpellLogic(self, actingHero, targetList):
        selectedTarget = self.chooseSpellTarget(actingHero, targetList)
        if selectedTarget:
            # Heals all heroes (one or more) who were assigned to be targets of the spell
            self.printSpellMessage(selectedTarget[0])
            for character in selectedTarget:
                cureHPValue = random.randint(self.spellPower, 2 * self.spellPower)
                Character.printAmountHealed(character, cureHPValue)
                time.sleep(0.5)
                # Heals the target hero, up to a maximum of their max HP value
                character.currentHP = min(character.maxHP, character.currentHP + cureHPValue)
                Character.printCurrentHP(character)
                time.sleep(1)
            return True
        return False


class CureSpell(HealingSpell):
    def __init__(self):
        super().__init__()
        self.spellPower = 30
        self.target = "One"
        self.name = "Cure"
        self.effect = "(Restores some HP to one hero)"

    @staticmethod
    def printSpellMessage(target):
        print("Little specks of light fill the air around " + target.name + ".")


class SanctuarySpell(HealingSpell):
    def __init__(self):
        super().__init__()
        self.spellPower = 12
        self.target = "All"
        self.name = "Sanctuary"
        self.effect = "(Restores low HP to all heroes)"

    @staticmethod
    def printSpellMessage(target):
        print("Beams of light fall down from the sky, illuminating the battlefield.")


class BuffSpell(Spell):
    def __init__(self):
        super().__init__()
        self.spellPower = 0
        self.alteredStat = None
        self.name = ""
        self.effect = ""

    # Controls the logic for all spells that increase a stat of the target
    def buffSpell(self, actingHero, targetList):
        selectedTarget = self.chooseSpellTarget(actingHero, targetList)
        if selectedTarget:
            # Buffs all heroes (one or more) who were assigned to be targets of the spell
            for character in selectedTarget:
                # Checks the stat that it should buff, and does so for all heroes (one or more) who were assigned to be
                # targets of the spell
                time.sleep(1)
                if self.alteredStat == "Defense":
                    # Increases the hero's defense by the spell's power
                    print("--" + character.name + "'s defense rose!")
                    character.defense += self.spellPower
            return True
        return False


class DamageSpell(Spell):
    def __init__(self):
        super().__init__()
        self.spellPower = 0
        self.spellAccuracy = 0
        self.spellElement = []

    # Controls the logic for all spells that decrease the target's HP
    def damageSpell(self, actingHero, targetList):
        selectedTarget = self.chooseSpellTarget(actingHero, targetList)
        if selectedTarget:
            # Damages all targets(one or more) who were assigned to be targets of the spell
            for character in selectedTarget:
                spellSuccess = self.shouldSpellHit(character)
                if self.spellElement in character.resistance:
                    damageValue = max(1, random.randint(self.spellPower // 2, self.spellPower))
                elif self.spellElement in character.weakness:
                    damageValue = random.randint(1.5 * self.spellPower, 3 * self.spellPower)
                else:
                    damageValue = random.randint(self.spellPower, 2 * self.spellPower)
                if spellSuccess and self.target == "One":
                    print(self.spellTextHit + character.name + self.secondaryTextHit)
                elif self.target == "One":
                    print(self.spellTextMiss + character.name + self.secondaryTextMiss)
                time.sleep(1)
                print("Enemy " + character.name + " takes " + str(damageValue) + " damage!")
                character.currentHP -= damageValue
                Character.isDead(character)
            return True
        return False


class DebuffSpell(Spell):
    def __init__(self):
        super().__init__()
        self.spellPower = 0
        self.spellAccuracy = 0
        self.spellElement = []
        self.alteredStat = None

    # Controls the logic for all spells that decrease a stat of the target's HP
    def debuffSpell(self, actingHero, targetList):
        selectedTarget = self.chooseSpellTarget(actingHero, targetList)
        if selectedTarget:
            # Damages all targets(one or more) who were assigned to be targets of the spell
            for character in selectedTarget:
                spellSuccess = self.shouldSpellHit(character)
                if spellSuccess and self.target == "One":
                    if self.alteredStat == "Hits":
                        # Decreases the target's hit count by the spell's power
                        print("--" + character.name + " ")
                        character.hitAmount = max(1, character.hitAmount * self.spellPower)
                elif self.target == "One":
                    print(self.spellTextMiss + character.name + self.secondaryTextMiss)
                time.sleep(1)
            return True
        return False


class StatusSpell(Spell):
    def __init__(self):
        super().__init__()
        self.spellAccuracy = 0
        self.spellElement = []
        self.status = []


class InstantDeathSpell(Spell):
    def __init__(self):
        super().__init__()
        self.spellAccuracy = 0
        self.spellElement = []


####################################
####################################
####################################


# Allows the player to choose the target of an attack, spell, item, etc.
def chooseTarget(actingHero, targetList):
    # Loops until the player chooses a legal target
    while True:
        print(actingHero.name + "! Choose your target:")
        time.sleep(0.5)
        # Prints all available targets, and the indices to each available target
        for index, target in enumerate(targetList):
            print("\t\t" + str(index + 1) + ". " + targetList.name)
        print("\t\tc. Cancel")
        targetChosen = input()
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(targetList):
            return int(targetChosen)
        elif targetChosen == "c".lower():
            return None
        else:
            print("That is not a valid response.")
            time.sleep(1)


# Takes a list of all enemies/heroes in the fight and returns a shuffled copy of that list
# Used for randomly determining who acts in what order in combat
def determineInitiative(combatantList):
    clonedInitiativeList = combatantList[:]
    random.shuffle(clonedInitiativeList)
    return clonedInitiativeList


# Prints the current round of combat and all surviving combatants on either side
def printCurrentRoundDetails(currentRound, heroList, enemyList):
    # Displays the current round
    print("\n\tROUND " + str(currentRound) + "!")
    time.sleep(2)
    # Displays all surviving combatants, putting a comma between them
    print(', '.join(str(combatant.name) for combatant in heroList))
    print("\t\tVS\n\t", end='')
    print(', '.join(str(combatant.name) for combatant in enemyList) + "\n")
    time.sleep(2)


# Controls the flow of combat between heroes and enemies
def combatSystem(heroList, enemyList):
    listOfCombatants = (heroList + enemyList)
    battleInProgress = True
    roundCount = 0
    livingEnemies = [enemy for enemy in enemyList if enemy.currentHP > 0]
    livingHeroes = [hero for hero in heroList if hero.currentHP > 0]
    for enemy in enemyList:
        enemy.currentHP = enemy.maxHP
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
                targetChosen = chooseTarget(currentActingCombatant, livingEnemies)
                # If the hero chooses to physically attack
                print(currentActingCombatant.name + " attacks enemy " + str(livingEnemies[targetChosen].name) + "!")
                time.sleep(1.5)
            # If the current attacker is an enemy and there are surviving heroes, they randomly attack one
            elif currentActingCombatant in livingEnemies and len(livingHeroes) > 0:
                targetChosen = random.randint(0, len(livingHeroes) - 1)
                print(currentActingCombatant.name + " attacks " + livingHeroes[targetChosen].name + "!")
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
# for hero in listOfParty:
#     hero.currentHP = hero.maxHP
#     hero.defense = hero.armor
#     hero.evasion = hero.agility
#     hero.damage = max(1, hero.strength // 2)
#     hero.accuracy = hero.hitRate


h1 = Fighter("Leo")
h2 = Fighter("Mike")
h3 = Fighter("Don")
h4 = Fighter("Raph")
e1 = Goblin("Bob")
e2 = Goblin("Rob")
e3 = Goblin("Klobb")

L1 = [h1, h2, h3, h4]
L2 = [e1, e2, e3]

combatSystem(L1, L2)