import random
import time
import collections


class Character:
    orderedSpellList = [SpellInstance.CURE, SpellInstance.FOG, SpellInstance.SANCTUARY, SpellInstance.FIRE,
                        SpellInstance.POISON_GAS, SpellInstance.SLOW, SpellInstance.HASTE, SpellInstance.STUN,
                        SpellInstance.SOFT, SpellInstance.CURSE, SpellInstance.DOOM, SpellInstance.BANE]

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
        self.speed = 0
        self.criticalChance = 0
        self.hitAmount = 1

        self.weakness = []
        self.resistance = []
        self.spellsKnown = collections.OrderedDict()
        self.status = []

    # Controls the logic and flow of a character's physical attack
    def attackTarget(self, target):
        timesAttackDone = 0
        # A character attacks once for each hitAmount they have
        while timesAttackDone < self.hitAmount:
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

    def shouldRun(self, listOfEnemies):
        listOfEnemySpeeds = [enemy.speed for enemy in listOfEnemies]
        maxEnemySpeed = max(listOfEnemySpeeds)
        if maxEnemySpeed > 200:
            return False
        randomCheckToRun = random.randint(0, 2 * maxEnemySpeed)
        if self.speed > randomCheckToRun:
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
        time.sleep(0.5)

    # Prints the character's current HP
    def printCurrentHP(self):
        print("--{}'s HP is now {}.".format(self.fullName, self.currentHP))
        time.sleep(0.3)

    # Prints that the target was killed
    def printDeathMessage(self):
        print("{} has fallen.".format(self.fullName))
        time.sleep(0.3)

    # Prints that the attacker missed
    def printAttackMiss(self):
        print("--{} missed!".format(self.fullName))
        time.sleep(0.3)

    # Prints the amount of HP that a character heals
    def printAmountHealed(self, healHPValue):
        print("--{} healed {} HP!".format(self.fullName, healHPValue))
        time.sleep(0.5)

    # Prints that a character's stat has increased
    def printStatBuffMessage(self, buffedStat):
        print("--{}'s {} has increased!".format(self.fullName, buffedStat.lower()))
        time.sleep(0.5)

    # Prints that a character's stat has decreased
    def printStatDebuffMessage(self, debuffedStat):
        print("--{}'s {} has gone down!".format(self.fullName, debuffedStat.lower()))
        time.sleep(0.5)

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
        elif statusToBuff == "Hit Amount":
            self.hitAmount += statValue
            time.sleep(1)

    # Decreases a particular stat of the character by a specific amount
    def debuffCharacter(self, statusToDebuff, statValue):
        if statusToDebuff == "Defense":
            self.defense = max(0, self.defense - statValue)
            time.sleep(1)
        elif statusToDebuff == "Hit Amount":
            self.hitAmount = max(1, self.hitAmount - statValue)
            time.sleep(1)

    # Returns a list of strings containing the spells a character knows and how many charges of that spell remain
    def getListOfKnownSpellsAndCharges(self):
        tempList = list(self.spellsKnown.items())
        for spell, charges in tempList:
            tempList[tempList.index((spell, charges))] = ["{} ({} charges remaining)".format(spell.name, charges)
                                                          if charges != 1 else "{} (1 charge"
                                                                               "remaining)".format(spell.name)]
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
        self.hitAmount = 1 + self.hitRate // 32
        self.accuracy = self.hitRate
        self.level = 1

    # TO WORK ON IN FUTURE
    # def chooseSpellToCast(self):
    #     orderedSpellList = [spell + " (1 charge remaining)" for spell in self.orderedSpellDictionary if spell in
    #                         self.spellsKnown.keys() and self.spellsKnown[spell] == 1]
    #     for index in range(len(orderedSpellList)):
    #         if
    #         orderedSpellList[index] += ""
    #     spellChargesList = [None] * len(orderedSpellList)
    #     for orderedSpellKey in self.orderedSpellDictionary:
    #         if orderedSpellKey in self
    #         spellChargesList[index] =
    #     for orderedSpellKey in self.orderedSpellDictionary:
    #         if orderedSpellKey in self.spellsKnown.keys() \
    #                 and not self.spellsKnown[orderedSpellKey] == 1:
    #             print("\t\t" + str(spellSelectionCount + 1) + ". " + orderedSpellKey + " (" +
    #                   str(self.spellsKnown[orderedSpellKey]) + " charges remaining)")
    #             spellSelectionCount += 1
    #         elif orderedSpellKey in self.spellsKnown.keys():
    #             print("\t\t" + str(spellSelectionCount + 1) + ". " + orderedSpellKey + " (1 charge remaining)")
    #             spellSelectionCount += 1
    #             # Tells the attack program to reiterate selecting an enemy if you cancel your spell

    # def castSpellLogic(self, heroList, enemyList):
    #     # Loops until the hero chooses a legal target
    #     tempSpellList = [spell for spell in self.orderedSpellDictionary if spell in self.spellsKnown.keys()]
    #     indexOfSpellChosen = self.chooseSpellToCast()
    #     spellChosen = tempSpellList[indexOfSpellChosen - 1]
    #     #  Tests if you have a charge remaining in that spell
    #     if indexOfSpellChosen:
    #         pass
    #     else:
    #         print("That is not a valid response.")
    #         time.sleep(1)


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
        self.luck = 9
        self.hitRate = 16
        self.speed = 5
        self.magicDef = 44
        self.criticalChance = 10
        self.spellsKnown = collections.OrderedDict([(SpellInstance.CURE, 2), (SpellInstance.FIRE, 2)])
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
        self.spellsKnown = collections.OrderedDict([(SpellInstance.CURE, 3), (SpellInstance.FOG, 2),
                                                    (SpellInstance.SANCTUARY, 2)])
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
        self.spellsKnown = collections.OrderedDict([(SpellInstance.FIRE, 3), (SpellInstance.POISON_GAS, 2),
                                                    (SpellInstance.SLOW, 2)])
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
        self.speed = 18
        self.magicDef = 16
        self.criticalChance = 4
        self.name = name


class Spell:
    def __init__(self):
        self.target = None
        self.targetParty = "Enemy"
        self.name = ""
        self.effect = ""
        self.spellPower = 0
        self.spellAccuracy = 0
        self.spellElement = []

    # Takes the selected spell and instigates the appropriate castSpell method from its particular class
    @staticmethod
    def castSpellSuperclassMethod(spellChosenIndex, actingHero, livingCombatants):
        spellChosen = list(actingHero.spellsKnown.keys())[spellChosenIndex]
        if spellChosen.targetParty == "Ally":
            targetList = [hero for hero in livingCombatants if isinstance(hero, Hero)]
        else:
            targetList = [enemy for enemy in livingCombatants if isinstance(enemy, Enemy)]
        spellChosenBoolean = spellChosen.castSpell(actingHero, targetList)
        # If the player chose a target for the spell, remove one charge from that spell and return True
        if spellChosenBoolean:
            actingHero.spellsKnown[spellChosen] -= 1
            return True
        # If the player cancelled the spell while selecting the target, return False
        return False

    # Determines if a spell should affect the target or not
    def shouldSpellHit(self, target):
        # The base chance to hit can be modified as needed
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

    # Returns a list of the string representation of all possible targets of the spell
    def getListOfPossibleTargets(self, targetList):
        # If the spell only targets one character, return the list that was passed
        if self.target == "One":
            return targetList
        # If the spell targets all heroes or enemies, return a list containing only the one appropriate string
        # representation
        elif isinstance(targetList[0], Enemy):
            return ["All enemies"]
        return ["All heroes"]

    # Returns a list of targets that the player chose, based on the string representations they were passed
    def getListOfSelectedTargets(self, targetList, targetIndex):
        # If the spell targets all heroes or enemies, return the list that was passed
        if self.target == "All":
            return targetList
        # If the spell only targets one character, return only the appropriate index of the list that was passed
        return [targetList[targetIndex]]

    # Returns a random integer between the spell's power and twice that amount
    def getRandomSpellPower(self):
        return random.randint(self.spellPower, 2 * self.spellPower)

    # The next three methods are passed, and only called in their overwritten forms in the subclasses as needed
    def printSpellMessage(self, caster, target):
        pass

    def printSpellMessageHit(self, caster, target):
        pass

    def printSpellMessageMiss(self, caster, target):
        pass


class HealingSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Ally"

    # Controls the logic for all spells that heal the target's HP
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = chooseTarget(actingHero, listOfPossibleTargets)
        if selectedTargetIndex:
            # Heals all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                healHPValue = self.getRandomSpellPower()
                Character.printAmountHealed(character, healHPValue)
                # Heals the target character, up to a maximum of their max HP value
                Character.healCharacter(character, healHPValue)
                Character.printCurrentHP(character)
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
    def printSpellMessage(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("Little specks of light fill the air around {}.".format(targetName))


class SanctuarySpell(HealingSpell):
    def __init__(self):
        super().__init__()
        self.spellPower = 12
        self.target = "All"
        self.name = "Sanctuary"
        self.effect = "(Restores low HP to all heroes)"

    @staticmethod
    def printSpellMessage(caster, target):
        print("Beams of light fall down from the sky, illuminating the battlefield.")


class BuffSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Ally"
        self.spellPower = 0
        self.alteredStat = None

    # Controls the logic for all spells that increase the target's stats
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = chooseTarget(actingHero, listOfPossibleTargets)
        if selectedTargetIndex:
            # Buffs the characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                # Some spells buff multiple stats at once
                for stat in self.alteredStat:
                    character.printStatBuffMessage(stat)
                    character.buffCharacter(stat, self.spellPower)
            return True
        return False


class FogSpell(BuffSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Fog"
        self.effect = "(Increases one hero's defense for the battle)"
        self.spellPower = 8
        self.alteredStat = ["Defense"]

    @staticmethod
    def printSpellMessage(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("A thick ethereal fog forms around {}, acting as a powerful shield!".format(targetName))


class HasteSpell(BuffSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Haste"
        self.effect = "(Increases one hero's amount of hits for the battle)"
        self.spellPower = 2
        self.alteredStat = ["Hit Amount"]

    @staticmethod
    def printSpellMessage(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("The air around {0} begins to blur, as {0} moves with renewed speed.".format(targetName))


class DamageSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"

    # Controls the logic for all spells that decrease the target's HP
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = chooseTarget(actingHero, listOfPossibleTargets)
        if selectedTargetIndex:
            # Damages all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                damageDealt = self.getRandomSpellPower()
                # Targets resistant to the spell take half damage.
                # Targets weak to the spell take 1.5 times the damage
                if character.isResistantToElement(self.spellElement):
                    damageDealt = max(1, damageDealt // 2)
                if character.isWeakToElement(self.spellElement):
                    damageDealt *= 1.5
                if self.shouldSpellHit(character):
                    self.printSpellMessageHit(actingHero, character)
                    character.applyDamage(damageDealt)
                # Damage spells can miss, which reduces the damage they do by half
                else:
                    damageDealt = max(1, damageDealt // 2)
                    self.printSpellMessageMiss(actingHero, character)
                    character.applyDamage(damageDealt)
            return True
        return False


class FireSpell(DamageSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Fire"
        self.effect = "(Causes fire-type damage to one enemy)"
        self.spellPower = 28
        self.spellAccuracy = 40
        self.spellElement = ["Fire"]

    @staticmethod
    def printSpellMessage(caster, target):
        casterName = "enemy " + caster.name if isinstance(caster, Enemy) else caster.name
        print("A fireball shoots out of {}'s hand.".format(casterName))

    @staticmethod
    def printSpellMessageHit(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("The fireball hits {}'s body directly!".format(targetName))

    @staticmethod
    def printSpellMessageMiss(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("The fireball barely singes {}.".format(targetName))


class PoisonGasSpell(DamageSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Poison Gas"
        self.effect = "(Causes low poison-type damage to all enemies)"
        self.spellPower = 12
        self.spellAccuracy = 20
        self.spellElement = ["Poison"]

    @staticmethod
    def printSpellMessage(caster, target):
        casterName = "Enemy " + caster.name if isinstance(caster, Enemy) else caster.name
        targetAffiliation = "your party" if isinstance(caster, Enemy) else "the enemies"
        print("{} raises their arms, and clouds of toxic gas surround {}.".format(casterName, targetAffiliation))


class DebuffSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"
        self.spellPower = 0
        self.alteredStat = []

    # Controls the logic for all spells that decrease a stat of the target's HP
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = chooseTarget(actingHero, listOfPossibleTargets)
        if selectedTargetIndex:
            # Debuffs the characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                if self.shouldSpellHit(character):
                    self.printSpellMessageHit(actingHero, character)
                    # Some spells debuff multiple stats at once
                    for stat in self.alteredStat:
                        character.printStatDebuffMessage(stat)
                        character.debuffCharacter(stat, self.spellPower)
                # Debuff spells can miss, which causes the spell to have no effect
                else:
                    self.printSpellMessageMiss(actingHero, character)
            return True
        return False


class SoftSpell(DebuffSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Soft"
        self.effect = "(Reduces the defensive power of all enemies)"
        self.spellPower = 4
        self.spellAccuracy = 40
        self.alteredStat = ["Defense"]

    @staticmethod
    def printSpellMessage(caster, target):
        casterName = "enemy " + caster.name if isinstance(caster, Enemy) else caster.name
        print("Wispy black smoke rises from {}, and quickly covers the battlefield.".format(casterName))

    @staticmethod
    def printSpellMessageHit(caster, target):
        print("{}'s armor becomes malleable and weak!".format(target.fullName))


class SlowSpell(DebuffSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Slow"
        self.effect = "(Reduces the amount of hits from one enemy)"
        self.spellPower = 2
        self.spellAccuracy = 64
        self.alteredStat = ["Hit Amount"]

    @staticmethod
    def printSpellMessage(caster, target):
        print("{} raises a hand to their mouth, muttering arcane words.".format(caster.fullName))

    @staticmethod
    def printSpellMessageHit(caster, target):
        print("{}'s body begins to significantly slow down.".format(target.fullName))

    @staticmethod
    def printSpellMessageMiss(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("The utterances seem to have no effect on {}.".format(targetName))


class StatusSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"
        self.status = []

    # Controls the logic for all spells that inflict a status effect on the target
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = chooseTarget(actingHero, listOfPossibleTargets)
        if selectedTargetIndex:
            # Applies the status to all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                if self.shouldSpellHit(character):
                    self.printSpellMessageHit(actingHero, character)
                    for statusEffect in self.status:
                        # Status spells add the status effect to the target's status effect list
                        # The only status that can occur multiple times in a target's status effect list is Doom
                        if statusEffect not in character.status or statusEffect == "Doom":
                            character.status.append(statusEffect)
                # Status spells can miss, which causes the spell to have no effect
                else:
                    self.printSpellMessageMiss(actingHero, character)
            return True
        return False


class StunSpell(StatusSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Stun"
        self.effect = "(Paralyzes one enemy)"
        self.spellAccuracy = 64
        self.spellElement = ["Status"]
        self.status = ["Paralysis"]

    @staticmethod
    def printSpellMessage(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("{} raises a hand, and dim specks of orange light appear around {}.".format(caster.fullName, targetName))

    @staticmethod
    def printSpellMessageHit(target):
        print("{}'s limbs begin to slow down, then begin to twitch violently.".format(target.fullName))

    @staticmethod
    def printSpellMessageMiss():
        print("The sparks fade within a second, and nothing seems to happen.")


class DoomSpell(StatusSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Doom"
        self.effect = "(Makes all enemies fall after three turns)"
        self.spellAccuracy = 30
        self.spellElement = ["Death"]
        self.status = [["Doom", "Doom", "Doom"]]

    @staticmethod
    def printSpellMessage(caster, target):
        targetAffiliation = "your party's" if isinstance(caster, Enemy) else "the enemies'"
        print("{} raises a hand and chants ominously... Spectral images of hourglasses flash in {}"
              "vision.".format(caster.fullName, targetAffiliation))


class InstantDeathSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"

    # Controls the logic for all spells that instantly set the target's HP to 0
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = chooseTarget(actingHero, listOfPossibleTargets)
        if selectedTargetIndex:
            # Kills all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                if self.shouldSpellHit(character):
                    self.printSpellMessageHit(actingHero, character)
                    character.currentHP = 0
                    character.printDeathMessage()
                # Instant death spells can miss, which causes the spell to have no effect
                else:
                    self.printSpellMessageMiss(actingHero, character)
            return True
        return False


class CurseSpell(InstantDeathSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Curse"
        self.effect = "(Makes one enemy immediately fall in battle)"
        self.spellAccuracy = 20
        self.spellElement = ["Death"]

    @staticmethod
    def printSpellMessage(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("{} drags a thumbnail across a wooden doll while staring at {}.".format(caster.fullName, targetName))

    @staticmethod
    def printSpellMessageHit(caster, target):
        targetName = "enemy " + target.name if isinstance(target, Enemy) else target.name
        print("A shadow passes over {}'s face... They suddenly fall down, completely still.".format(targetName))

    @staticmethod
    def printSpellMessageMiss(caster, target):
        print("The wooden doll splinters with no effect.")


class BaneSpell(InstantDeathSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Bane"
        self.effect = "(Makes all enemies immediately fall in battle)"
        self.spellAccuracy = 8
        self.spellElement = ["Poison", "Death"]

    @staticmethod
    def printSpellMessage(caster, target):
        print("{} spreads their arms to either side, and thick purple mist covers the"
              "battlefield.".format(caster.fullName))


class SpellInstance:
    CURE = CureSpell()
    FOG = FogSpell()
    SANCTUARY = SanctuarySpell()
    HASTE = HasteSpell()
    FIRE = FireSpell()
    POISON_GAS = PoisonGasSpell()
    SLOW = SlowSpell()
    STUN = StunSpell()
    SOFT = SoftSpell()
    CURSE = CurseSpell()
    DOOM = DoomSpell()
    BANE = BaneSpell()


class StatusEffect:
    def __init__(self, name):
        self.name = name
        self.endsAfterBattle = True

    def isIncapacitated(self):
        if self.name in ["Stone"]:
            return True
        return False

    def cannotAct(self):
        if self.name in ["Paralysis", "Sleep"]:
            return True
        return False

    def applyStatusDamage(self, character):
        pass

    # Prints that a character has died from the Doom status
    def printDoomMessage(self, character):
        print("--{}'s lifeline has been cut short by dark magic.".format(character.fullName))
        time.sleep(0.5)
        character.printDeathMessage()

    # Controls the logic for the Doom status effect
    def controlDoomStatusLogic(self, character):
        # If the character has Doom in their status list, remove it from the list
        sublist = isInList(character.status, "Doom")
        if sublist:
            sublist.remove("Doom")
            # If that was the last copy of Doom in their status list, that character dies and a message prints
            if "Doom" not in sublist:
                character.currentHP = 0
                character.printDoomMessage()


class ParalysisStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class PoisonStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class StoneStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class BlindStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class MuteStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class SleepStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class ConfusionStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class DoomStatus(StatusEffect):
    def __init__(self):
        super().__init__()


class HolyStatus(StatusEffect):
    def __init__(self):
        super().__init__()


####################################
####################################
####################################


def isInList(listOfLists, searchedQuery):
    for specificList in listOfLists:
        if searchedQuery in specificList:
            return specificList


# Allows the player to choose the target of an attack, spell, item, etc.
def chooseTarget(actingHero, targetList, choice="target"):
    # Loops until the player chooses a legal target
    while True:
        print("{}! Choose your {}:".format(actingHero.name, choice))
        time.sleep(0.5)
        # Prints all available targets, and the indices to each available target
        for index, target in enumerate(targetList):
            print("\t\t{}. {}".format(index + 1, target.name))
        print("\t\tc. Cancel")
        targetChosen = input()
        # Returns the chosen index, or None if the player chose to cancel the action
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(targetList):
            return int(targetChosen)
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


def chooseTurnAction(actingHero, livingEnemies, livingHeroes):
    listOfOptions = ["Attack", "Cast a spell", "Use an item", "Run away"]
    while True:
        print("{}! Choose your action:".format(actingHero.name))
        time.sleep(0.5)
        # Prints all available targets, and the indices to each available target
        for index, option in enumerate(listOfOptions):
            print("\t\t{}. {}".format(index + 1, option))
        targetChosen = input()
        # Returns the chosen index, or None if the player chose to cancel the action
        if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(listOfOptions):
            actionChosenBoolean = controlActionChoiceLogic(actingHero, livingEnemies, livingHeroes,
                                                           int(targetChosen) - 1)
            if actionChosenBoolean:
                break
        else:
            print("That is not a valid response.")
            time.sleep(1)


def controlActionChoiceLogic(actingHero, livingEnemies, livingHeroes, actionChosen):
    # If the hero chooses to physically attack
    if actionChosen == 1:
        targetChosen = chooseTarget(actingHero, livingEnemies)
        if targetChosen:
            print("{} attacks enemy {}!".format(actingHero.name, livingEnemies[targetChosen].name))
            time.sleep(1.5)
            actingHero.attackTarget(livingEnemies[targetChosen])
            return True
    # If the hero chooses to cast a spell
    elif actionChosen == 2:
        actingHero.reorderCharacterSpellDict()
        spellListWithCharges = actingHero.getListOfKnownSpellsAndCharges()
        spellChosen = chooseTarget(actingHero, spellListWithCharges, "spell")
        if spellChosen:
            livingCombatants = livingHeroes + livingEnemies
            spellCastBoolean = Spell.castSpellSuperclassMethod(spellChosen - 1, actingHero, livingCombatants)
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
        print("You couldn't escape!")
        return True
    return False


# Controls the flow of combat between heroes and enemies
def controlCombatSystemLogic(heroList, enemyList):
    listOfCombatants = (heroList + enemyList)
    battleInProgress = True
    roundCount = 0
    for enemy in enemyList:
        enemy.currentHP = enemy.maxHP
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
                targetChosen = chooseTarget(currentActingCombatant, livingEnemies)
                # If the hero chooses to physically attack
                print("{} attacks enemy {}!").format(currentActingCombatant.name, livingEnemies[targetChosen].name)
                time.sleep(1.5)
            # If the current attacker is an enemy and there are surviving heroes, they randomly attack one
            elif currentActingCombatant in livingEnemies and len(livingHeroes) > 0:
                targetChosen = random.randint(0, len(livingHeroes) - 1)
                print("{} attacks {}!").format(currentActingCombatant.name, livingHeroes[targetChosen].name)
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


# h1 = Fighter("Leo")
# h2 = Fighter("Mike")
# h3 = Fighter("Don")
# h4 = Fighter("Raph")
# e1 = Goblin("Bob")
# e2 = Goblin("Rob")
# e3 = Goblin("Klobb")
#
# L1 = [h1, h2, h3, h4]
# L2 = [e1, e2, e3]
#
# for hero in L1:
#     hero.currentHP = hero.maxHP
# controlCombatSystemLogic(L1, L2)
