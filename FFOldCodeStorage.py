import random
import time

# Change all globals
# For i in range BB


class Character:
    def __init__(self):
        self.maxHP = 0
        self.currentHP = 0
        self.damage = 0
        self.defense = 0
        self.magicDef = 0
        self.evasion = 0
        self.accuracy = 0
        self.critChance = 0
        self.weakness = ''
        self.resistance = ''
        self.spellsKnown = {}
        self.orderedSpellDictionary = ["Cure", "Fog", "Sanctuary", "Fire", "Poison Smoke", "Slow", "Stun", "Curse",
                                       "Hex"]
        self.status = ''
        self.canAct = True
        self.isDead = False
        self.name = ''

    def attack(self, target):
        # The attacking combatant will randomly hit or miss, based on the target's evasion
        # Incapacitated targets cannot dodge
        # baseChanceToHit can be altered to fit new statuses as they are coded in (e.g., blindness reduces it)
        hitAmount = 1
        timesAttackDone = 0
        if isinstance(self, Hero):
            hitAmount = 1 + self.hitRate // 32
            if isinstance(self, Monk):
                hitAmount *= 2
        while timesAttackDone in range(hitAmount):
            baseChanceToHit = 168
            toHit = baseChanceToHit + self.accuracy - target.evasion
            randomCheckToHit = random.randint(1, 200)
            if randomCheckToHit > toHit and target.canAct == True:
                if isinstance(self, Enemy):
                    print("--Enemy " + str(self) + " missed!")
                else:
                    print("--" + self.name + " missed!")
            else:
                self.applyDamage(target)
                if target.currentHP == 0:
                    break

    def applyDamage(self, target):
        # Damage is a random number influenced by the attacker's damage score and the target's defense score
        # Damage has a minimum value of 1
        penetratedDamage = random.randint(self.damage - target.defense, (2 * self.damage) - target.defense)
        damage = max(1, penetratedDamage)
        # Critical hits should happen (critChance/2)% of the time
        criticalHitDiceRoll = random.randint(1, 200)
        if criticalHitDiceRoll <= self.critChance:
            # Critical hits do additional damage that bypasses defense
            damage += random.randint(self.damage, 2 * self.damage)
            time.sleep(0.5)
            print("--Critical hit!")
            time.sleep(1)
        target.currentHP -= damage

        # Displays damage taken
        # If target was a hero, displays target's current HP, minimum value of 0
        if isinstance(target, Enemy):
            print("--Enemy " + str(target) + " takes " + str(damage) + " damage.")
        else:
            print("--" + target.name + " takes " + str(damage) + " damage.")
            time.sleep(0.5)
            print("--" + target.name + "'s HP is now " + str(max(0, target.currentHP)) + ".")

            # If the enemy has a paralyzing touch, the hero might be paralyzed (unless they're already paralyzed or
            # dead)
            # Paraylzed heroes can't act. Paralysis is resisted with magic defense
            if "'paralysis'" in self.contactStatus:
                paralysisCheck = random.randint(1, 100)
                if paralysisCheck >= target.magicDef and target.currentHP > 0 and not "'paralysis'" in target.status:
                    print(target.name + " has been paralyzed!")
                    target.status += "'paralysis'"
                    target.canAct = False
        Character.deathCheck(target)

    # Test if the target is killed by the attack
    def deathCheck(self):
        if self.currentHP <= 0:
            self.currentHP = 0
            time.sleep(1)
            # Enemies are removed from their group once they have 0 HP
            if isinstance(self, Enemy):
                print("--Enemy " + str(self) + " has fallen.")
                listOfEnemies.remove(self)
                if not listOfEnemies:
                    time.sleep(2)
                    # Printed if all enemies have fallen
                    print("\n\t\tVictory!")
                    Hero.postCombat()
            # Heroes are removed from their group once they have 0 HP.
            if isinstance(self, Hero):
                print("--" + self.name + " has fallen.")
                listOfParty.remove(self)
                if not listOfParty:
                    time.sleep(2)
                    # Printed if all enemies have fallen
                    print("\n\t\tYou have been defeated. The princess is lost.")


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
        self.accuracy = self.hitRate

    def heroChooseAttackTarget(self, listOfParty, listOfEnemies):
        # Loops until the hero chooses a legal target
        while True:
            print(self.name + "! Choose your target:")
            time.sleep(0.5)
            # Prints all living enemies, and the indices to target each enemy
            for livingEnemy in listOfEnemies:
                    print("\t" + str(listOfEnemies.index(livingEnemy) + 1) + ". " + str(livingEnemy))
            # Only gives the hero the option to cast a spell if they know magic and have remaining spell charges
            if self.spellsKnown and not all(spellCharges == 0 for spellCharges in self.spellsKnown.values()):
                print("\ts. Use a spell")
            # Allows the player to check their party's class/job, current HP, and known spells
            print("\ti. Inspect your party")
            targetChosen = input()
            if targetChosen == 'i'.lower():
                for combatant in listOfParty:
                    print("\t\t" + combatant.name + " (" + str(combatant) + "): " + str(combatant.currentHP) + "/"
                          + str(combatant.maxHP))
                    # Shows the spells the hero knows, in a specific order, and how many charges of that spell remain
                    if combatant.spellsKnown:
                        time.sleep(0.5)
                        for orderedSpellKey in combatant.orderedSpellDictionary:
                            if orderedSpellKey in combatant.spellsKnown.keys()\
                                    and not combatant.spellsKnown[orderedSpellKey] == 1:
                                print("\t\t\t" + orderedSpellKey + " (" + str(combatant.spellsKnown[orderedSpellKey]) +
                                      " charges remaining)")
                            elif orderedSpellKey in combatant.spellsKnown.keys():
                                print("\t\t\t" + orderedSpellKey + " (1 charge remaining)")
                        time.sleep(2)
                    time.sleep(1)
                time.sleep(1)
            # Allows the player to cast a spell if they have any spell charges remaining
            elif targetChosen == 's'.lower() and self.spellsKnown \
                    and not all(spellCharges == 0 for spellCharges in self.spellsKnown.values()):
                temporaryListOfCombatants = listOfParty + listOfEnemies
                didNotCancelSpell = self.castASpell(temporaryListOfCombatants)
                if didNotCancelSpell:
                    break
            # Recognizes the target enemy the hero chose to attack, or repeats the loop if the hero chose an invalid
            # target
            elif targetChosen.isnumeric():
                targetChosenInteger = int(targetChosen) - 1
                if 0 <= targetChosenInteger < len(listOfEnemies):
                    return targetChosenInteger
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            else:
                print("That is not a valid response.")
                time.sleep(1)
    # Controls the logic behind all spell casting
    def castASpell(self, listOfCombatants):
        # Associates the order of spells in the orderedSpellDictionary with the spell functions
        # The dictionaryOfSpellFunctions only associates spells that heroes can cast, not enemy-exclusive spells
        dictionaryOfSpellFunctions = {0: CureSpell.healSpell(cureInstance, self, listOfCombatants),
                                      1: FogSpells.buffSpell(fogInstance, self, listOfCombatants),
                                      2: SanctuarySpell.healSpell(sanctuaryInstance, self, listOfCombatants),
                                      3: FireSpell.damageSpell(fireInstance, self, listOfCombatants),
                                      4: PoisonSpell.damageSpell(poisonInstance, self, listOfCombatants),
                                      5: SlowSpell.debuffSpell(slowInstance, self, listOfCombatants)}
        # Loops until the hero chooses a legal target
        while True:
            spellSelectionCount = 0
            print("Choose a spell:")
            # Shows spells the hero knows, in a specific order, and how many charges of that spell remain (enumerated)
            for orderedSpellKey in self.orderedSpellDictionary:
                if orderedSpellKey in self.spellsKnown.keys() \
                        and not self.spellsKnown[orderedSpellKey] == 1:
                    print("\t\t" + str(spellSelectionCount + 1) + ". " + orderedSpellKey + " (" +
                          str(self.spellsKnown[orderedSpellKey]) + " charges remaining)")
                    spellSelectionCount += 1
                elif orderedSpellKey in self.spellsKnown.keys():
                    print("\t\t" + str(spellSelectionCount + 1) + ". " + orderedSpellKey + " (1 charge remaining)")
                    spellSelectionCount += 1
            # Tells the attack program to reiterate selecting an enemy if you cancel your spell
            print("\t\tc. Cancel")
            spellSelectionChosen = input()
            if spellSelectionChosen == 'c'.lower():
                return False

            # Recognizes the spell the hero chose to cast, or repeats the loop if the hero chose an invalid target
            elif spellSelectionChosen.isnumeric():
                spellSelectionChosenInteger = int(spellSelectionChosen) - 1
                if 0 <= spellSelectionChosenInteger < len(self.spellsKnown):
                    # Ensures that the enumerated choice corresponds to the proper spell in the orderedSpellDictionary
                    temporarySpellList = []
                    for iterateSpells in self.orderedSpellDictionary:
                        if iterateSpells in self.spellsKnown.keys():
                            temporarySpellList.append(iterateSpells)
                    spellChosen = temporarySpellList[spellSelectionChosenInteger]
                    indexOfSpellChosen = self.orderedSpellDictionary.index(spellChosen)
                    #  Tests if you have a charge remaining in that spell
                    if self.spellsKnown[spellChosen] > 0:
                        spellCasting = dictionaryOfSpellFunctions[indexOfSpellChosen]
                        if spellCasting:
                            return True
                    # If not, it tells you that you can't cast the spell and reititates the loop to select a spell
                    else:
                        print("You cannot cast that spell now.")
                        time.sleep(1)
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            else:
                print("That is not a valid response.")
                time.sleep(1)

    @staticmethod
    def postCombat():
        print()
        for hero in listOfParty:
            hero.defense = hero.armor
            hero.evasion = hero.agility
            hero.damage = max(1, hero.strength // 2)
            hero.accuracy = hero.hitRate
            print(hero.name + "'s HP is now " + str(hero.currentHP) + "/" + str(hero.maxHP) + ".")
            time.sleep(1)

    @staticmethod
    def potionHealing():
        print()
        while True:
            if inventory["Potion"] > 1:
                print("Would you like to use a potion to fully heal a hero? You have " + str(inventory["Potion"])
                  + " potions left.")
            else:
                print("Would you like to use a potion to fully heal a hero? You have 1 potion left.")
            print("\t1. Yes\n\t2. No")
            potionChoice = input()
            if potionChoice == "1":
                while True:
                    print("Who would you like to use it on?")
                    time.sleep(0.5)
                    for hero in listOfParty:
                        print("\t" + str(listOfParty.index(hero) + 1) + ". " + hero.name + "  (" +
                              str(hero.currentHP) + "/" + str(hero.maxHP) + ")")
                    print("\tc. Cancel")
                    potionTarget = input()
                    if potionTarget == 'c':
                        return False
                    elif potionTarget.isnumeric():
                        potionTargetInteger = int(potionTarget) - 1
                        if 0 <= potionTargetInteger < len(listOfParty):
                            listOfParty[potionTargetInteger].currentHP = listOfParty[potionTargetInteger].maxHP
                            print(listOfParty[potionTargetInteger].name + " is fully healed! HP is now " +
                                  str(listOfParty[potionTargetInteger].maxHP) + ".")
                            inventory["Potion"] -= 1
                            time.sleep(2)
                            return True
                        else:
                            print("That is not a valid response.")
                            time.sleep(1)
                    else:
                        print("That is not a valid response.")
                        time.sleep(1)
            elif potionChoice == "2":
                return False
            else:
                print("That is not a valid response.")
                time.sleep(1)


class Fighter(Hero):
    # Represents a 'Fighter' type hero
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
        self.critChance = 10
        self.name = name


class Thief(Hero):
    # Represents a 'Thief' type hero
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
        self.critChance = 40
        self.name = name


class Monk(Hero):
    # Represents a 'Monk' type hero
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
        self.critChance = 8
        self.name = name


class RedMage(Hero):
    # Represents a 'Red Mage' type hero
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
        self.critChance = 10
        self.spellsKnown = {"Cure": 2, "Fire": 2}
        self.name = name


class WhiteMage(Hero):
    # Represents a 'White Mage' type hero
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
        self.critChance = 5
        self.spellsKnown = {"Cure": 3, "Fog": 2, "Sanctuary": 2}
        self.name = name


class BlackMage(Hero):
    # Represents a 'Black Mage' type hero
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
        self.critChance = 15
        self.spellsKnown = {"Fire": 3, "Poison Smoke": 2, "Slow": 2}
        self.name = name


class Enemy(Character):
    def __init__(self):
        Character.__init__(self)
        self.currentHP = self.maxHP
        self.contactStatus = ''
        self.spellChance = 0

    def castSpell(self, listOfCombatants):
        dictionaryOfSpellFunctions = {6: Spells.stunSpell, 7: Spells.curseSpell, 8: Spells.hexAllSpell}
        spellChoiceRandom = random.randint(1, len(self.spellsKnown)) - 1
        spellChosen = self.spellsKnown[spellChoiceRandom]
        indexOfSpellChosen = self.orderedSpellDictionary.index(spellChosen)
        dictionaryOfSpellFunctions[indexOfSpellChosen](self, listOfCombatants)


class Goblin(Enemy):
    # Represents a 'Goblin' type enemy
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
        self.critChance = 4
        self.name = name


class Bandit(Enemy):
    # Represents a 'Bandit' type enemy
    def __repr__(self):
        return "Bandit"

    def __init__(self, name="Bandit"):
        super().__init__()
        self.maxHP = 24
        self.damage = 12
        self.defense = 5
        self.evasion = 9
        self.accuracy = 12
        self.magicDef = 25
        self.critChance = 8
        self.name = name


class Zombie(Enemy):
    def __repr__(self):
        return "Zombie"

    def __init__(self, name="Zombie"):
        super().__init__()
        self.maxHP = 45
        self.damage = 12
        self.defense = 0
        self.evasion = 9
        self.accuracy = 8
        self.magicDef = 25
        self.critChance = 4
        self.weakness = 'Fire'
        self.resistance = 'Poison'
        self.contactStatus = "'paralysis'"
        self.name = name


class EvilKnight(Enemy):
    def __repr__(self):
        return "Garland"

    def __init__(self, name="Evil Knight Garland"):
        super().__init__()
        self.maxHP = 200
        self.damage = 18
        self.defense = 8
        self.evasion = 12
        self.accuracy = 35
        self.magicDef = 50
        self.critChance = 6
        self.spellChance = 35
        self.spellsKnown = ["Stun", "Curse", "Hex"]
        self.name = name


class Spells:
    def __init__(self):
        self.spellPower = 0
        self.spellAccuracy = 0
        self.target = ''
        self.spellElement = ''
        self.name = ''
        self.spellText = ''
        self.alteredStat = ''
        self.secondaryTextHit = '.'
        self.secondaryTextMiss = ''
        self.tertiaryTextHit = ''
        self.tertiaryTextMiss = ''

    # Controls the logic for all spells that heal the HP of heroes
    def healSpell(self, actingHero, targetList):
        # Makes a temporary list of just the heroes in combat
        temporaryHeroList = []
        for heroCharacter in targetList:
            if isinstance(heroCharacter, Hero):
                temporaryHeroList.append(heroCharacter)
        # Loop reiterates until the player chooses a valid target
        while True:
            selectedTargetOfSpell = []
            spellTargetIsSelected = False
            print("Choose the target for your " + self.name + " spell " + self.effect)
            # If the spell only targets one hero, prints an enumerated list of all living heroes
            if self.target == 'One Hero':
                for heroCharacter in temporaryHeroList:
                    print("\t\t" + str(temporaryHeroList.index(heroCharacter) + 1) + ". " + heroCharacter.name)
                print("\t\tc. Cancel")
                targetHeroInput = input()
                # Recognizes the player's input and relates it to the target hero
                if targetHeroInput.isnumeric():
                    targetHeroInteger = int(targetHeroInput) - 1
                    if 0 <= targetHeroInteger < len(temporaryHeroList):
                        selectedTargetOfSpell.append(temporaryHeroList[targetHeroInteger])
                        # Provides unique flavor text for the spell, ending with the target hero's name
                        print(self.spellText + selectedTargetOfSpell[0].name + self.secondaryTextHit)
                        time.sleep(1)
                        spellTargetIsSelected == True
                    else:
                        print("That is not a valid response.")
                        time.sleep(1)
                    # Returns to the attack selection phase if the player cancels the spell
                elif targetHeroInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            # If the spell targets all of your heroes, give the player only the option to select all heroes, or the
            # option to cancel
            elif self.target == 'All Heroes':
                print("\t\t1. All heroes")
                print("\t\tc. Cancel")
                targetHeroInput = input()
                # Recognizes the player's input and relates it to the target hero
                if targetHeroInput == "1":
                    for heroCharacter in temporaryHeroList:
                        selectedTargetOfSpell.append(heroCharacter)
                    print(self.spellText)
                    time.sleep(1)
                    spellTargetIsSelected == True
                # Returns to the attack selection phase if the player cancels the spell
                elif targetHeroInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            if spellTargetIsSelected:
                # Removes one charge of the spell being cast
                actingHero.spellsKnown[self.name] -= 1
                cureHPValue = random.randint(self.spellPower, 2 * self.spellPower)
                # Heals all heroes (one or more) who were assigned to be targets of the spell
                for heroCharacter in selectedTargetOfSpell:
                    print("--" + heroCharacter.name + " healed " + str(cureHPValue) + " HP!")
                    time.sleep(0.5)
                    # Heals the target hero, up to a maximum of their max HP value
                    heroCharacter.currentHP = min(heroCharacter.maxHP, heroCharacter.currentHP + cureHPValue)
                    print("--" + heroCharacter.name + "'s HP is now " + str(heroCharacter.currentHP) + "!")
                    time.sleep(1)
                    return True

    # Controls the logic for all spells that buff the stats of heroes
    def buffSpell(self, actingHero, targetList):
        # Makes a temporary list of just the heroes in combat
        temporaryHeroList = []
        for heroCharacter in targetList:
            if isinstance(heroCharacter, Hero):
                temporaryHeroList.append(heroCharacter)
        # Loop reiterates until the player chooses a valid target
        while True:
            selectedTargetOfSpell = []
            spellTargetIsSelected = False
            print("Choose the target for your " + self.name + " spell " + self.effect)
            # If the spell only targets one hero, prints an enumerated list of all living heroes
            if self.target == 'One Hero':
                for heroCharacter in temporaryHeroList:
                    print("\t\t" + str(temporaryHeroList.index(heroCharacter) + 1) + ". " + heroCharacter.name)
                print("\t\tc. Cancel")
                targetHeroInput = input()
                # Recognizes the player's input and relates it to the target hero
                if targetHeroInput.isnumeric():
                    targetHeroInteger = int(targetHeroInput) - 1
                    if 0 <= targetHeroInteger < len(temporaryHeroList):
                        selectedTargetOfSpell.append(temporaryHeroList[targetHeroInteger])
                        # Provides unique flavor text for the spell, ending with the target hero's name
                        print(self.spellText + selectedTargetOfSpell[0].name + self.secondaryTextHit)
                        time.sleep(1)
                        spellTargetIsSelected == True
                    else:
                        print("That is not a valid response.")
                        time.sleep(1)
                        # Returns to the attack selection phase if the player cancels the spell
                elif targetHeroInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            # If the spell targets all of your heroes, give the player only the option to select all heroes, or the
            # option to cancel
            elif self.target == 'All Heroes':
                print("\t\t1. All heroes")
                print("\t\tc. Cancel")
                targetHeroInput = input()
                # Recognizes the player's input and relates it to the target hero
                if targetHeroInput == "1":
                    for heroCharacter in temporaryHeroList:
                        selectedTargetOfSpell.append(heroCharacter)
                    print(self.spellText)
                    time.sleep(1)
                    spellTargetIsSelected == True
                # Returns to the attack selection phase if the player cancels the spell
                elif targetHeroInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            if spellTargetIsSelected:
                # Removes one charge of the spell being cast
                actingHero.spellsKnown[self.name] -= 1
                # Checks the stat that it should buff, and does so for all heroes (one or more) who were assigned to be
                # targets of the spell
                if self.alteredStat == 'Defense':
                    # Increases the hero's defense by the spell's power
                    for heroCharacter in selectedTargetOfSpell:
                        heroCharacter.defense += self.spellPower
                    return True

    # Controls the logic for all spells that damage the enemies
    def damageSpell(self, actingHero, targetList):
        # Makes a temporary list of just the enemies in combat
        temporaryEnemyList = []
        for enemyCharacter in targetList:
            if isinstance(enemyCharacter, Enemy):
                temporaryEnemyList.append(enemyCharacter)
        # Loop reiterates until the player chooses a valid target
        while True:
            selectedTargetOfSpell = []
            spellTargetIsSelected = False
            print("Choose the target for your " + self.name + " spell " + self.effect)
            # If the spell only targets one enemy, prints an enumerated list of all living enemies
            if self.target == 'One Enemy':
                for enemyCharacter in temporaryEnemyList:
                    print("\t\t" + str(temporaryEnemyList.index(enemyCharacter) + 1) + ". " + str(enemyCharacter))
                print("\t\tc. Cancel")
                targetEnemyInput = input()
                # Recognizes the player's input and relates it to the target enemy
                if targetEnemyInput.isnumeric():
                    targetEnemyInteger = int(targetEnemyInput) - 1
                    if 0 <= targetEnemyInteger < len(temporaryEnemyList):
                        selectedTargetOfSpell.append(temporaryEnemyList[targetEnemyInteger])
                        time.sleep(1)
                        spellTargetIsSelected == True
                    else:
                        print("That is not a valid response.")
                        time.sleep(1)
                    # Returns to the attack selection phase if the player cancels the spell
                elif targetEnemyInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            # If the spell targets all of enemies, give the player only the option to select all enemies, or the
            # option to cancel
            elif self.target == 'All Enemies':
                print("\t\t1. All enemies")
                print("\t\tc. Cancel")
                targetEnemyInput = input()
                # Recognizes the player's input and relates it to the target hero
                if targetEnemyInput == "1":
                    for enemyCharacter in temporaryEnemyList:
                        selectedTargetOfSpell.append(enemyCharacter)
                    time.sleep(1)
                    spellTargetIsSelected == True
                # Returns to the attack selection phase if the player cancels the spell
                elif targetEnemyInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            if spellTargetIsSelected:
                # Removes one charge of the spell being cast
                actingHero.spellsKnown[self.name] -= 1
                # Damage received is a random number between the spell's power and twice its power
                # Enemies resistant to the element take half damage, enemies weak to the element take 1.5 times damage
                # And other enemies take standard damage.
                for enemyCharacter in selectedTargetOfSpell:
                    if enemyCharacter.resistance == self.spellElement:
                        damageValue = max(1, random.randint(self.spellPower // 2, self.spellPower))
                    elif enemyCharacter.weakness == self.spellElement:
                        damageValue = random.randint(1.5 * self.spellPower, 3 * self.spellPower)
                    else:
                        damageValue = random.randint(self.spellPower, 2 * self.spellPower)
                    # Calculates if the spell directly hits the enemy, or if it just passes them
                    # Resistant enemies are very unlikely to be hit directly
                    # Weak enemies are more likely to be hit directly by the spell
                    # Spell accuracy and the target's magic defense influences if the spell hits directly or not
                    baseChanceToHit = 148
                    if enemyCharacter.resistance == self.spellElement:
                        baseChanceToHit = 0
                    if enemyCharacter.weakness == self.spellElement:
                        baseChanceToHit += 40
                    spellToHit = baseChanceToHit + self.spellAccuracy - enemyCharacter.magicDef
                    randomCheckToHit = random.randint(1, 200)
                    # Provides a unique flavor text for each enemy
                    # The text's format depends on if the spell targets one enemy or all, and if it hits directly
                    if randomCheckToHit < spellToHit:
                        if self.target == 'One Enemy':
                            print(self.spellText + actingHero.name + self.secondaryTextHit + str(enemyCharacter) +
                                  self.tertiaryTextHit)
                        else:
                            print(self.spellText + actingHero.name + self.secondaryTextHit)
                    elif self.target == 'One Enemy':
                        print(self.spellText + actingHero.name + self.secondaryTextMiss + str(enemyCharacter) +
                                  self.tertiaryTextMiss)
                    else:
                        print(self.spellText + actingHero.name + self.secondaryTextMiss)
                    time.sleep(1)
                    print("Enemy " + str(enemyCharacter) + " takes " + str(damageValue) + " damage!")
                    Character.deathCheck(enemyCharacter)
                    return True

    # Controls the logic for all spells that debuff the stats of the enemies
    def debuffSpell(self, actingHero, targetList):
        # Makes a temporary list of just the enemies in combat
        temporaryEnemyList = []
        for enemyCharacter in targetList:
            if isinstance(enemyCharacter, Enemy):
                temporaryEnemyList.append(enemyCharacter)
        # Loop reiterates until the player chooses a valid target
        while True:
            selectedTargetOfSpell = []
            spellTargetIsSelected = False
            print("Choose the target for your " + self.name + " spell " + self.effect)
            # If the spell only targets one enemy, prints an enumerated list of all living enemies
            if self.target == 'One Enemy':
                for enemyCharacter in temporaryEnemyList:
                    print("\t\t" + str(temporaryEnemyList.index(enemyCharacter) + 1) + ". " + str(enemyCharacter))
                print("\t\tc. Cancel")
                targetEnemyInput = input()
                # Recognizes the player's input and relates it to the target enemy
                if targetEnemyInput.isnumeric():
                    targetEnemyInteger = int(targetEnemyInput) - 1
                    if 0 <= targetEnemyInteger < len(temporaryEnemyList):
                        selectedTargetOfSpell.append(temporaryEnemyList[targetEnemyInteger])
                        time.sleep(1)
                        spellTargetIsSelected == True
                    else:
                        print("That is not a valid response.")
                        time.sleep(1)
                    # Returns to the attack selection phase if the player cancels the spell
                elif targetEnemyInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            # If the spell targets all of enemies, give the player only the option to select all enemies, or the
            # option to cancel
            elif self.target == 'All Enemies':
                print("\t\t1. All enemies")
                print("\t\tc. Cancel")
                targetEnemyInput = input()
                # Recognizes the player's input and relates it to the target hero
                if targetEnemyInput == "1":
                    for enemyCharacter in temporaryEnemyList:
                        selectedTargetOfSpell.append(enemyCharacter)
                    time.sleep(1)
                    spellTargetIsSelected == True
                # Returns to the attack selection phase if the player cancels the spell
                elif targetEnemyInput == 'c'.lower():
                    return False
                else:
                    print("That is not a valid response.")
                    time.sleep(1)
            if spellTargetIsSelected:
                # Removes one charge of the spell being cast
                actingHero.spellsKnown[self.name] -= 1
                for enemyCharacter in selectedTargetOfSpell:
                    # Calculates if the spell affects the enemy or not
                    # Resistant enemies are very unlikely to be affected
                    # Weak enemies are more likely to be affected
                    # Spell accuracy and the target's magic defense influences if the spell takes effect or not
                    baseChanceToHit = 148
                    if enemyCharacter.resistance == self.spellElement:
                        baseChanceToHit = 0
                    if enemyCharacter.weakness == self.spellElement:
                        baseChanceToHit += 40
                    spellToHit = baseChanceToHit + self.spellAccuracy - enemyCharacter.magicDef
                    randomCheckToHit = random.randint(1, 200)
                    # Provides a unique flavor text for each enemy
                    # The text's format depends on if the spell targets one enemy or all, and if it hits directly
                    if randomCheckToHit < spellToHit:
                        if self.target == 'One Enemy':
                            print(self.spellText + actingHero.name + self.secondaryTextHit + str(enemyCharacter) +
                                  self.tertiaryTextHit)
                            if self.alteredStat == "Damage":
                                enemyCharacter.damage -= self.spellPower
                        else:
                            print(self.spellText + actingHero.name + self.secondaryTextHit)
                    elif self.target == 'One Enemy':
                        print(self.spellText + actingHero.name + self.secondaryTextMiss + str(enemyCharacter) +
                                  self.tertiaryTextMiss)
                    else:
                        print(self.spellText + actingHero.name + self.secondaryTextMiss)
                    time.sleep(1)
                    return True


    @staticmethod
    def stunSpell(actingEnemy, targetList):
            temporaryHeroList = []
            for hero in targetList:
                if isinstance(hero, Hero):
                    temporaryHeroList.append(hero)
            targetChosen = random.randint(0, len(temporaryHeroList) - 1)
            print(str(actingEnemy) + " casts a spell on " + temporaryHeroList[targetChosen].name + "!")
            time.sleep(3)
            print("--" + temporaryHeroList[targetChosen].name + " is surrounded by dim, orange specks of light...")
            time.sleep(3)
            spellToHit = 165 - temporaryHeroList[targetChosen].magicDef
            randomCheckToHit = random.randint(1, 200)
            if randomCheckToHit < spellToHit and "'paralysis'" not in temporaryHeroList[targetChosen].status:
                print("--" +  temporaryHeroList[targetChosen].name + "'s limbs begin to slow down, then begin to twitch"
                                                             " violently.")
                time.sleep(2)
                print("--" + temporaryHeroList[targetChosen].name + " has been paralyzed!")
                temporaryHeroList[targetChosen].status += "'paralysis'"
                temporaryHeroList[targetChosen].canAct = False
            else:
                print("--But nothing seems to happen!")
            time.sleep(3)

    @staticmethod
    def curseSpell(actingEnemy, targetList):
            temporaryHeroList = []
            for hero in targetList:
                if isinstance(hero, Hero):
                    temporaryHeroList.append(hero)
            targetChosen = random.randint(0, len(temporaryHeroList) - 1)
            print(str(actingEnemy) + " casts a spell on " + temporaryHeroList[targetChosen].name + "!")
            time.sleep(3)
            print("--" + temporaryHeroList[targetChosen].name + "'s armor begins to glow a dark purple!")
            time.sleep(3)
            spellToHit = 165 - temporaryHeroList[targetChosen].magicDef
            randomCheckToHit = random.randint(1, 200)
            if randomCheckToHit < spellToHit:
                print("--" + temporaryHeroList[targetChosen].name + "'s armor fades away, crumbling into dust!")
                temporaryHeroList[targetChosen].defense = 0
            else:
                print("--But nothing seems to happen!")
            time.sleep(3)


    @staticmethod
    def hexAllSpell(actingEnemy, targetList):
            print(str(actingEnemy) + " casts a spell on all heroes!")
            temporaryHeroList = []
            for hero in targetList:
                if isinstance(hero, Hero):
                    temporaryHeroList.append(hero)
            time.sleep(3)
            print("--Wispy black smoke begins to rise from the heroes' armor!")
            time.sleep(3)
            for hero in temporaryHeroList:
                spellToHit = 165 - hero.magicDef
                randomCheckToHit = random.randint(1, 200)
                if randomCheckToHit < spellToHit:
                    print("--Cracks and dents appear across " + hero.name + "'s armor, weakening it significantly!")
                    hero.defense = max(0, hero.defense - 4)
                else:
                    print("--The smoke fades away from " + hero.name + "'s armor with no visible effect!")
                time.sleep(3)
            time.sleep(1)

class CureSpell(Spells):
    def __init__(self):
        super().__init__()
        self.spellPower = 30
        self.target = 'One Hero'
        self.name = 'Cure'
        self.effect = '(Restores some HP to one hero)'
        self.spellText = 'Little specks of light fill the air around '

class FogSpell(Spells):
    def __init__(self):
        super().__init__()
        self.spellPower = 8
        self.alteredStat = 'Defense'
        self.target = 'One Hero'
        self.name = 'Fog'
        self.effect = '(Increases defense for the battle)'
        self.spellText = 'A thick ethereal fog forms around '
        self.secondaryTextHit = ', acting as a powerful shield!'

class SanctuarySpell(Spells):
    def __init__(self):
        super().__init__()
        self.spellPower = 12
        self.target = 'All Heroes'
        self.name = 'Sanctuary'
        self.effect = '(Restores low HP to all heroes)'
        self.spellText = 'Beams of light fall down from the sky, surrounding your party.'

class FireSpell(Spells):
    def __init__(self):
        super().__init__()
        self.spellAccuracy = 24
        self.spellPower = 25
        self.spellElement = 'Fire'
        self.target = 'One Enemy'
        self.name = 'Fire'
        self.effect = '(Causes some fire-type damage to one enemy)'
        self.spellText = 'A fireball shoots out of '
        self.secondaryTextHit = "'s hand and hits enemy "
        self.tertiaryTextHit = " head-on!"
        self.secondaryTextMiss = "'s hand, but barely singes enemy "
        self.tertiaryTextMiss = "."

class PoisonSpell(Spells):
    def __init__(self):
        super().__init__()
        self.spellAccuracy = 24
        self.spellPower = 10
        self.alteredStat = 'Damage'
        self.target = 'One Enemy'
        self.name = 'Slow'
        self.effect = '(Causes low poison-type damage to all enemies)'
        self.secondaryTextHit = " raises his arms, and clouds of toxic gas surround the enemies!"
        self.secondaryTextMiss = self.secondaryTextHit

class SlowSpell(Spells):
    def __init__(self):
        super().__init__()
        self.spellPower = 64
        self.alteredStat = 'Damage'
        self.target = 'One Enemy'
        self.name = 'Slow'
        self.effect = '(Reduces the strength of one enemy)'
        self.secondaryTextHit = "chants for a moment... Suddenly, "
        self.tertiaryTextHit = "'s body seems to slow down!"
        self.secondaryTextMiss = "chants for a moment... But nothing seems to happen to enemy "


########################################################

def main():
    print("The kingdom has been betrayed!")
    time.sleep(1)
    print("The good princess Sara has been kidnapped by Garland, one of the king's high knights!")
    time.sleep(1)
    print("He has hired monsters and mercenaries to wait on the trail, killing any who dare try to catch him.")
    time.sleep(1)
    print("Only you ")
    print("Choose four heroes! Fight evil monsters! Save the princess!")
    time.sleep(1)
    print("\tFighters are physically strong, dealing high damage and resisting the most damage.")
    time.sleep(1.5)
    print("\tThieves have a high evasion score and crit rate, frequently dodging attacks and scoring bonus damage.")
    time.sleep(1.5)
    print("\tMonks have the highest HP, surviving long battles, and attack twice as often as other heroes.")
    time.sleep(1.5)
    print("\tRed Mages only have moderate physical stats, but have access to a cure spell and a fire spell.")
    time.sleep(1.5)
    print("\tWhite Mages are weak in combat, but can boost your heroes' defense and restore HP.")
    time.sleep(1.5)
    print("\tBlack Mages are incredibly weak physically, but can decimate foes with their powerful magic.")
    print()

    # Chooses the four hero types for your party, appending them to the (initially empty) party list
    baseListOfParty = []
    heroesInPartyAmount = 0
    while heroesInPartyAmount < 4:
        baseListOfParty.append(addingHeroesToParty(heroesInPartyAmount))
        print("You have chosen a " + str(baseListOfParty[heroesInPartyAmount]) + ".")
        time.sleep(1)
        print("Please type in a name for your " + str(baseListOfParty[heroesInPartyAmount]) + " (Max 4 letters)")
        heroName = input()
        while len(heroName) > 4:
            print("I'm sorry, that name is too long.")
            time.sleep(0.5)
            print(
                "Please type in a name for your " + str(baseListOfParty[heroesInPartyAmount]) + " (Max 4 letters)")
            heroName = input()
        baseListOfParty[heroesInPartyAmount].name = heroName
        heroesInPartyAmount += 1

    print("Your party is:")
    for hero in range(baseListOfParty):
        print(baseListOfParty[heroesInPartyAmount].name + " (" + str(baseListOfParty[heroesInPartyAmount]) + ")")

########################################################


# Allows you to select the four heroes that make up your party
def addingHeroesToParty(heroNumber):
    # The six heroes you can choose
    dictionaryOfHeroes = {"f": Fighter(), "t": Thief(), "m": Monk(), "r": RedMage(), "w": WhiteMage(),
                          "b": BlackMage()}
    heroNumberList = ["first", "second", "third", "last"]
    print("Type the first letter of the class you want your " + heroNumberList[heroNumber] + " character to be.")
    heroChoice = input().lower()

    # This block loops each time you give an invalid input
    while heroChoice not in dictionaryOfHeroes.keys():
        print("That is not a valid response.")
        time.sleep(0.5)
        print("Type the first letter of the class you want your " + heroNumberList[heroNumber] + " character to be.")
        heroChoice = input().lower()
    # Returns the hero corresponding to your input
    return dictionaryOfHeroes[heroChoice]


############################


# Takes a list of all enemies/heroes in the fight and returns a shuffled copy of that list
# Used for randomly determining who acts in what order in combat
def determineInitiative(listOfAllCombatants):
    clonedInitiativeList = listOfAllCombatants[:]
    random.shuffle(clonedInitiativeList)
    return clonedInitiativeList


# Controls the flow of combat between heroes and enemies
def combatSystem(listOfParty, listOfEnemies):
    listOfCombatants = (listOfParty + listOfEnemies)
    battleInProgress = True
    roundCount = 0
    for enemy in listOfEnemies:
        enemy.currentHP = enemy.maxHP
    while battleInProgress:
        roundCount += 1
        # Each round, randomizes the order in which combatants act
        currentRoundInitiative = determineInitiative(listOfCombatants)

        # Keeps track of the round of combat
        print("\n\t\t\tROUND " + str(roundCount) + "!")
        time.sleep(2)

        # Displays all surviving combatants, putting a comma between them
        for combatant in listOfParty[:-1]:
            print(combatant.name + ", ",  end='')
        print(listOfParty[-1].name, end='')
        print("    VS    ", end='')
        for combatant in listOfEnemies[:-1]:
            print(combatant.name + ", ",  end='')
        print(listOfEnemies[-1].name + "\n")
        time.sleep(2)

        # Each combatants acts in the randomized initiative order
        for turnOrder in range(len(listOfCombatants)):
            # If the current attacker is a hero and there are surviving enemies, they are given a list of all
            # surviving enemies, and choose which one to attack
            if currentRoundInitiative[turnOrder] in listOfParty and len(listOfEnemies) > 0:
                if "'paralysis'" in currentRoundInitiative[turnOrder].status:
                    paralysisCheck = random.randint(1, 4)
                    if paralysisCheck == 1:
                        print(currentRoundInitiative[turnOrder].name + " can't move!")
                        targetChosen = ''
                    else:
                        print(currentRoundInitiative[turnOrder].name + " is no longer paralyzed!")
                        currentRoundInitiative[turnOrder].status = \
                            currentRoundInitiative[turnOrder].status.replace("'paralysis'", "")
                        currentRoundInitiative[turnOrder].canAct = True
                        targetChosen = ''
                elif currentRoundInitiative[turnOrder].canAct:
                    targetChosen = Hero.heroChooseAttackTarget(currentRoundInitiative[turnOrder], listOfParty,
                                                           listOfEnemies)
                # If the hero chooses to physically attack
                if targetChosen or targetChosen == 0:
                    print(currentRoundInitiative[turnOrder].name + " attacks enemy "
                          + str(listOfEnemies[targetChosen]) + "!")
                    time.sleep(0.5)
                    currentRoundInitiative[turnOrder].attack(listOfEnemies[targetChosen])

            # If the current attacker is an enemy and there are surviving heroes, they randomly attack one
            elif currentRoundInitiative[turnOrder] in listOfEnemies and len(listOfParty) > 0:
                spellCheck = random.randint(1, 100)
                if currentRoundInitiative[turnOrder].spellChance >= spellCheck:
                    Enemy.castSpell(currentRoundInitiative[turnOrder], listOfCombatants)
                else:
                    targetChosen = random.randint(0, len(listOfParty) - 1)
                    print(str(currentRoundInitiative[turnOrder]) + " attacks " + listOfParty[targetChosen].name + "!")
                    time.sleep(0.5)
                    currentRoundInitiative[turnOrder].attack(listOfParty[targetChosen])

            # Iterates through every combatant in the randomized initiative order
            turnOrder += 1
            # Only pauses if the current attacker is alive
            # (This prevents long strings of pauses as more and more combatants die)
            if currentRoundInitiative[turnOrder - 1] in listOfParty\
                    or currentRoundInitiative[turnOrder - 1] in listOfEnemies:
                time.sleep(2)

            # The battle ends once one side is completely defeated
            if listOfEnemies == [] or listOfParty == []:
                battleInProgress = False


# if __name__ == '__main__':  # del
#    main()  # del


cureInstance = CureSpell()
fogInstance = FogSpell()
sanctuaryInstance = CureSpell()
fireInstance = FireSpell()
poisonInstance = PoisonSpell()
slowInstance = SlowSpell()

hero1 = Fighter("Fitr")   # del
hero2 = BlackMage("Blak")   # del
hero3 = Monk("Monk")   # del
hero4 = RedMage("Red")   # del
inventory = {"Potion": 2}
baseListOfParty = [hero1, hero2, hero3, hero4]   # del
listOfParty = []
for character in baseListOfParty:
    listOfParty.append(character)

for hero in listOfParty:
    hero.currentHP = hero.maxHP
    hero.defense = hero.armor
    hero.evasion = hero.agility
    hero.damage = max(1, hero.strength // 2)
    hero.accuracy = hero.hitRate

print("BATTLE!")
time.sleep(1)
print("Three goblins attack!")
time.sleep(1)
listOfEnemies = [Goblin() for n in range(3)]
combatSystem(listOfParty, listOfEnemies)
potionNotFinished = True
while inventory["Potion"] > 0 and potionNotFinished:
    potionNotFinished = Hero.potionHealing()
time.sleep(2)
print()

print("BATTLE!")
time.sleep(1)
print("Five goblins attack!")
time.sleep(1)
listOfEnemies = [Goblin() for n in range(5)]
combatSystem(listOfParty, listOfEnemies)
potionNotFinished = True
for hero in listOfParty:
    if hero.temporaryDefensiveChange != 0:
        hero.defense = hero.temporaryDefensiveChange
while inventory["Potion"] > 0 and potionNotFinished:
    potionNotFinished = Hero.potionHealing()
time.sleep(2)
print()

print("BATTLE!")
time.sleep(1)
print("Two goblins and two bandits attack!")
time.sleep(1)
listOfEnemies = [Goblin() for n in range(2)] + [Bandit() for n in range(2)]
combatSystem(listOfParty, listOfEnemies)
potionNotFinished = True
for hero in listOfParty:
    if hero.temporaryDefensiveChange != 0:
        hero.defense = hero.temporaryDefensiveChange
while inventory["Potion"] > 0 and potionNotFinished:
    potionNotFinished = Hero.potionHealing()
time.sleep(2)
print()

print("BATTLE!")
time.sleep(1)
print("Two zombies attack!")
time.sleep(1)
listOfEnemies = [Zombie() for n in range(2)]
combatSystem(listOfParty, listOfEnemies)
potionNotFinished = True
for hero in listOfParty:
    if hero.temporaryDefensiveChange != 0:
        hero.defense = hero.temporaryDefensiveChange
while inventory["Potion"] > 0 and potionNotFinished:
    potionNotFinished = Hero.potionHealing()
time.sleep(2)
print()

print("BATTLE!")
time.sleep(1)
print("The evil knight appears! End him, and rescue the princess!")
time.sleep(1)
listOfEnemies = [EvilKnight()]
combatSystem(listOfParty, listOfEnemies)
potionNotFinished = True
