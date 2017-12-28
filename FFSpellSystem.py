import random
import time
import FFBattleSystem


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
            targetList = [hero for hero in livingCombatants if isinstance(hero, FFBattleSystem.Hero)]
        else:
            targetList = [enemy for enemy in livingCombatants if isinstance(enemy, FFBattleSystem.Enemy)]
        spellChosenBoolean = spellChosen.castSpell(actingHero, targetList)
        # If the player chose a target for the spell, remove one charge from that spell and return True
        if spellChosenBoolean:
            if spellChosen.name == "Armageddon":
                actingHero.spellsKnown[spellChosen][0] = 1
            actingHero.spellsKnown[spellChosen][0] -= 1
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
        elif isinstance(targetList[0], FFBattleSystem.Enemy):
            return ["All enemies"]
        return ["All heroes"]

    def chooseSpellTarget(self, targetList):
        # Loops until the player chooses a legal target
        while True:
            print("Choose the target for your {} spell!  {}".format(self.name, self.effect))
            time.sleep(1)
            # Prints all available targets, and the indices to each available target
            for index, target in enumerate(targetList):
                if isinstance(target, list):
                    print("\t\t{}. {}".format(index + 1, target[0].name))
                else:
                    print("\t\t{}. {}".format(index + 1, target))
            print("\t\tc. Cancel")
            targetChosen = input()
            # Returns the chosen index, or None if the player chose to cancel the action
            if targetChosen.isnumeric() and 0 < int(targetChosen) <= len(targetList):
                return int(targetChosen)
            elif targetChosen.lower() == "c":
                return None
            else:
                print("That is not a valid response.")
                time.sleep(1)

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
        selectedTargetIndex = self.chooseSpellTarget(listOfPossibleTargets)
        if selectedTargetIndex:
            # Heals all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                healHPValue = self.getRandomSpellPower()
                FFBattleSystem.Character.printAmountHealed(character, healHPValue)
                # Heals the target character, up to a maximum of their max HP value
                FFBattleSystem.Character.healCharacter(character, healHPValue)
                FFBattleSystem.Character.printCurrentHP(character)
            return True
        return False


class CureSpell(HealingSpell):
    def __init__(self):
        super().__init__()
        self.spellPower = 30
        self.target = "One"
        self.name = "Cure"
        self.effect = "(Restores some HP to one hero)"

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("Little specks of light fill the air around {}.".format(targetName))
        time.sleep(1)


class SanctuarySpell(HealingSpell):
    def __init__(self):
        super().__init__()
        self.spellPower = 12
        self.target = "All"
        self.name = "Sanctuary"
        self.effect = "(Restores low HP to all heroes)"

    def printSpellMessage(self, caster, target):
        print("Beams of light fall down from the sky, illuminating the battlefield.")
        time.sleep(1)


class BuffSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Ally"
        self.spellPower = 0
        self.alteredStat = None

    # Controls the logic for all spells that increase the target's stats
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = self.chooseSpellTarget(listOfPossibleTargets)
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

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("A thick ethereal fog forms around {}, acting as a powerful shield!".format(targetName))
        time.sleep(1)


class HasteSpell(BuffSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Haste"
        self.effect = "(Increases one hero's strike count for the battle)"
        self.spellPower = 2
        self.alteredStat = ["Strike Count"]

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("The air around {0} begins to blur, as {0} moves with renewed speed.".format(targetName))
        time.sleep(1)


class DamageSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"

    # Controls the logic for all spells that decrease the target's HP
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = self.chooseSpellTarget(listOfPossibleTargets)
        if selectedTargetIndex:
            # Damages all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            for character in listOfSelectedTargets:
                damageDealt = self.getRandomSpellPower()
                if self.name == "Armageddon":
                    damageDealt += random.randint(0, 10) * actingHero.spellsKnown[self][0]
                if self.name == "Judgment":
                    self.spellPower *= 1.5
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
                if character.isIncapacitated():
                    character.printDeathMessage()
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

    def printSpellMessage(self, caster, target):
        casterName = "enemy " + caster.name if isinstance(caster, FFBattleSystem.Enemy) else caster.name
        print("A fireball shoots out of {}'s hand.".format(casterName))
        time.sleep(1)

    def printSpellMessageHit(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("--The fireball hits {}'s body directly!".format(targetName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("--The fireball barely singes {}.".format(targetName))
        time.sleep(1)


class PoisonGasSpell(DamageSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Poison Gas"
        self.effect = "(Causes low poison-type damage to all enemies)"
        self.spellPower = 12
        self.spellAccuracy = 20
        self.spellElement = ["Poison"]

    def printSpellMessage(self, caster, target):
        targetAffiliation = "your party" if isinstance(caster, FFBattleSystem.Enemy) else "the enemies"
        print("{} raises their arms, and clouds of toxic gas surround {}.".format(caster.fullName, targetAffiliation))
        time.sleep(1)


class ArmageddonSpell(DamageSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Armageddon"
        self.effect = "(Can only be cast once per day, but devastates the enemy forces)"
        self.spellPower = 35
        self.spellAccuracy = 40
        self.spellElement = []

    def printSpellMessage(self, caster, target):
        casterName = "enemy " + caster.name if isinstance(caster, FFBattleSystem.Enemy) else caster.name
        targetAffiliation = "your party" if isinstance(caster, FFBattleSystem.Enemy) else "the enemies"
        print("{} channels all of their strength... With a mighty cry from {}, fires rise from the earth "
              "below {}.".format(caster.fullName, casterName, targetAffiliation))
        if isinstance(caster, FFBattleSystem.Hero):
            caster.currentHP = 1
        time.sleep(1)


class JudgmentSpell(DamageSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Judgment"
        self.effect = "(Unleashes God's wrath upon an enemy. Becomes stronger over time.)"
        self.spellPower = 40
        self.spellAccuracy = 35
        self.spellElement = []

    def printSpellMessage(self, caster, target):
        casterName = "enemy " + caster.name if isinstance(caster, FFBattleSystem.Enemy) else caster.name
        print("{} chants as clouds gather overhead... With a mighty cry from {}, lightning rains down from the "
              "heavens towards {}.".format(caster.fullName, casterName, target.fullName))
        if isinstance(caster, FFBattleSystem.Hero):
            caster.currentHP = 1
        time.sleep(1)


class DebuffSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"
        self.spellPower = 0
        self.alteredStat = []

    # Controls the logic for all spells that decrease a stat of the target's HP
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = self.chooseSpellTarget(listOfPossibleTargets)
        if selectedTargetIndex:
            # Debuffs the characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            missedAllTargets = True
            for character in listOfSelectedTargets:
                if self.shouldSpellHit(character):
                    self.printSpellMessageHit(actingHero, character)
                    # Some spells debuff multiple stats at once
                    for stat in self.alteredStat:
                        character.printStatDebuffMessage(stat)
                        character.debuffCharacter(stat, self.spellPower)
                    missedAllTargets = False
                # Debuff spells can miss, which causes the spell to have no effect
                elif self.target == "One":
                    self.printSpellMessageMiss(actingHero, character)
                    missedAllTargets = False
            if missedAllTargets:
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

    def printSpellMessage(self, caster, target):
        casterName = "enemy " + caster.name if isinstance(caster, FFBattleSystem.Enemy) else caster.name
        print("Wispy black smoke rises from {}, and quickly covers the battlefield.".format(casterName))
        time.sleep(1)

    def printSpellMessageHit(self, caster, target):
        print("--{}'s armor becomes malleable and weak!".format(target.fullName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        print("--But it soon fades away with no effect.")
        time.sleep(1)


class SlowSpell(DebuffSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Slow"
        self.effect = "(Reduces the strike count of one enemy)"
        self.spellPower = 2
        self.spellAccuracy = 64
        self.alteredStat = ["Strike Count"]

    def printSpellMessage(self, caster, target):
        print("{} raises a hand to their mouth, muttering arcane words.".format(caster.fullName))
        time.sleep(1)

    def printSpellMessageHit(self, caster, target):
        print("--{}'s body begins to significantly slow down.".format(target.fullName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("--The utterances seem to have no effect on {}.".format(targetName))
        time.sleep(1)


class BeaconSpell(DebuffSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Beacon"
        self.effect = "(Reduces the evasion of one enemy)"
        self.spellPower = 10
        self.spellAccuracy = 40
        self.alteredStat = ["Evasion"]

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("{} pulls some soft pebbles from their pocket and tosses them towards {}.".format(caster.fullName,
                                                                                                targetName))
        time.sleep(1)

    def printSpellMessageHit(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("--The stones stick to {}'s body and glow, attracting all further attacks.".format(targetName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("--The stones bounce off harmlessly.".format(targetName))
        time.sleep(1)


class StatusSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"
        self.status = []

    # Controls the logic for all spells that inflict a status effect on the target
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = self.chooseSpellTarget(listOfPossibleTargets)
        if selectedTargetIndex:
            # Applies the status to all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            missedAllTargets = True
            for character in listOfSelectedTargets:
                if self.shouldSpellHit(character):
                    self.printSpellMessageHit(actingHero, character)
                    for statusEffect in self.status:
                        # Status spells add the status effect to the target's status effect list
                        # The only status that can occur multiple times in a target's status effect list is Doom
                        if statusEffect not in character.status or statusEffect == "Doom":
                            character.status.append(statusEffect)
                    missedAllTargets = False
                # Status spells can miss, which causes the spell to have no effect
                elif self.target == "One":
                    self.printSpellMessageMiss(actingHero, character)
                    missedAllTargets = False
            if missedAllTargets:
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

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("{} raises a hand, and dim specks of orange light appear around {}.".format(caster.fullName, targetName))
        time.sleep(1)

    def printSpellMessageHit(self, caster, target):
        print("--{}'s limbs begin to slow down, then begin to twitch violently.".format(target.fullName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        print("--The sparks fade within a second, and nothing seems to happen.")
        time.sleep(1)


class SilenceSpell(StatusSpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.name = "Silence"
        self.effect = "(Silences one enemy, preventing them from casting spells)"
        self.spellAccuracy = 44
        self.spellElement = ["Status"]
        self.status = ["Silence"]

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("{} waves their hand, and bright white lights begin to spiral around {}.".format(caster.fullName,
                                                                                               targetName))
        time.sleep(1)

    def printSpellMessageHit(self, caster, target):
        print("--{} has been surrounded by a circle of silence, from which no sound can "
              "escape.".format(target.fullName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        print("--{} lets out a cry of rage.".format(target.fullName))
        time.sleep(1)


class DoomSpell(StatusSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Doom"
        self.effect = "(Makes all enemies fall after three turns)"
        self.spellAccuracy = 30
        self.spellElement = ["Death"]
        self.status = [["Doom", "Doom", "Doom"]]

    def printSpellMessage(self, caster, target):
        targetAffiliation = "your party's" if isinstance(caster, FFBattleSystem.Enemy) else "the enemies'"
        print("{} raises a hand and chants ominously... Spectral images of hourglasses flash in {}"
              " vision.".format(caster.fullName, targetAffiliation))
        time.sleep(1)


class InstantDeathSpell(Spell):
    def __init__(self):
        super().__init__()
        self.targetParty = "Enemy"

    # Controls the logic for all spells that instantly set the target's HP to 0
    def castSpell(self, actingHero, targetList):
        listOfPossibleTargets = self.getListOfPossibleTargets(targetList)
        selectedTargetIndex = self.chooseSpellTarget(listOfPossibleTargets)
        if selectedTargetIndex:
            # Kills all characters (one or more) who were assigned to be targets of the spell
            listOfSelectedTargets = self.getListOfSelectedTargets(targetList, selectedTargetIndex - 1)
            self.printSpellMessage(actingHero, listOfSelectedTargets[0])
            missedAllTargets = True
            for character in listOfSelectedTargets:
                if self.shouldSpellHit(character):
                    self.printSpellMessageHit(actingHero, character)
                    character.currentHP = 0
                    character.printDeathMessage()
                    missedAllTargets = False
                # Instant death spells can miss, which causes the spell to have no effect
                elif self.target == "One":
                    self.printSpellMessageMiss(actingHero, character)
                    missedAllTargets = False
            if missedAllTargets:
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

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("{} makes a mark on a wooden doll while looking at {}.".format(caster.fullName, targetName))
        time.sleep(1)

    def printSpellMessageHit(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("--A shadow passes over {}'s face... They suddenly fall down, completely still.".format(targetName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        print("--The wooden doll splits in two, with no effect.")
        time.sleep(1)


class BaneSpell(InstantDeathSpell):
    def __init__(self):
        super().__init__()
        self.target = "All"
        self.name = "Bane"
        self.effect = "(Makes all enemies immediately fall in battle)"
        self.spellAccuracy = 8
        self.spellElement = ["Poison", "Death"]

    def printSpellMessage(self, caster, target):
        print("{} spreads their arms to either side, and thick purple mist covers the"
              " battlefield.".format(caster.fullName))
        time.sleep(1)

    def printSpellMessageMiss(self, caster, target):
        targetAffiliation = "Your party seems" if isinstance(caster, FFBattleSystem.Enemy) else "The enemies seem"
        print("{} to be unphased by the mist.".format(target.fullName, targetAffiliation))
        time.sleep(1)


class AuxiliarySpell(Spell):
    def __init__(self):
        super().__init__()


class PurgeSpell(AuxiliarySpell):
    def __init__(self):
        super().__init__()
        self.target = "One"
        self.targetParty = "Ally"
        self.name = "Purge"
        self.effect = "(Purges a hero of most negative status effects)"

    def castSpell(self, actingHero, targetList):
        selectedTargetIndex = self.chooseSpellTarget(targetList)
        if selectedTargetIndex:
            # Heals all negative non-KO, non-Doom status effects
            tempStatus = []
            self.printSpellMessage(actingHero, targetList[selectedTargetIndex - 1])
            for status in targetList[selectedTargetIndex - 1].status:
                if status in ["KO", "Stone", "Doom"]:
                    tempStatus.append(status)
                else:
                    print("{}'s body is purged of its {}.".format(targetList[selectedTargetIndex - 1].name, status))
                    time.sleep(0.5)
            if targetList[selectedTargetIndex - 1].status == tempStatus:
                print("But there are no negative status effects that {}'s magic can purge.".format(actingHero.name))
            targetList[selectedTargetIndex - 1].status = tempStatus
            time.sleep(1)
            return True
        return False

    def printSpellMessage(self, caster, target):
        targetName = "enemy " + target.name if isinstance(target, FFBattleSystem.Enemy) else target.name
        print("Light shines from within {}, causing them to briefly glow.".format(targetName))
        time.sleep(1)


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
    ARMAGEDDON = ArmageddonSpell()
    JUDGMENT = JudgmentSpell()
    BEACON = BeaconSpell()
    SILENCE = SilenceSpell()
    PURGE = PurgeSpell()
