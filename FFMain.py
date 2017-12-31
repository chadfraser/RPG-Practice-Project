import time
import FFBattleSystem
import FFSpellSystem
import FFLevelSystem
import FFItemSystem
import FFEquipmentSystem
import FFStatusSystem


def chooseStartingParty(listOfParty):
    # The six heroes you can choose
    dictionaryOfHeroes = {"f": FFBattleSystem.Fighter, "t": FFBattleSystem.Thief, "m": FFBattleSystem.Monk,
                          "r": FFBattleSystem.RedMage, "w": FFBattleSystem.WhiteMage,
                          "b": FFBattleSystem.BlackMage}
    heroOrdinalList = ["first", "second", "third", "last"]
    for heroOrdinal in heroOrdinalList:
        while True:
            print("Type the first letter of the class you want your {} character to be, or type 'h' for "
                  "help.".format(heroOrdinal))
            heroChoice = input().lower()
            if heroChoice in dictionaryOfHeroes.keys():
                print("You have chosen a {}.".format(dictionaryOfHeroes[heroChoice]()))
                heroName = chooseHeroName(dictionaryOfHeroes[heroChoice])
                heroCreated = dictionaryOfHeroes[heroChoice](heroName)
                listOfParty.append(heroCreated)
                FFBattleSystem.Hero.playerStartingParty.append(heroCreated)
                break
            if heroChoice == "h":
                printHelpMessage()
            else:
                print("That is not a valid response.")
                time.sleep(1)
    return listOfParty


def chooseHeroName(hero):
    while True:
        print("Please type in a name for your {} (Max 8 letters)".format(hero()))
        heroName = input()
        if len(heroName) > 8:
            print("I'm sorry, that name is too long.")
            time.sleep(0.5)
        else:
            return heroName


def main():
    listOfParty = chooseStartingParty([])
    for hero in listOfParty:
        hero.currentHP = hero.maxHP
        hero.setHeroDefaultValues()
    FFBattleSystem.startCombat(listOfParty, [FFBattleSystem.Goblin()])


def printHelpMessage():
    input("\tPress the enter key to navigate through the help text.")
    input("\tFighters are physically strong and can use most kinds of weapons and armor.")
    input("\tThieves are fast and evasive, and are more likely to score critical hits than other classes.")
    input("\tMonks get twice as many attacks off as the other heroes, and do not need weapons or armor.")


if __name__ == "__main__":
    main()


# e1 = FFBattleSystem.Goblin()
# e2 = FFBattleSystem.Goblin()
# e3 = FFBattleSystem.Goblin()
# enemiesList = [e1, e2, e3]
# h1 = FFBattleSystem.Monk()
# h2 = FFBattleSystem.BlackMage()
# h3 = FFBattleSystem.WhiteMage()
# h4 = FFBattleSystem.BlackMage()
# heroesList = [h1, h2, h3, h4]
# for hero in heroesList:
#     hero.currentHP = hero.maxHP
#     hero.setHeroDefaultValues()
#
# h1.spellsKnown[FFSpellSystem.SpellInstance.HASTE] = [4, 4]
# h2.spellsKnown[FFSpellSystem.SpellInstance.STUN] = [4, 4]
# h2.spellsKnown[FFSpellSystem.SpellInstance.SOFT] = [4, 4]
# h1.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]
# h2.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]
# h3.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]
# h4.spellsKnown[FFSpellSystem.SpellInstance.CURSE] = [4, 4]
# h2.spellsKnown[FFSpellSystem.SpellInstance.BANE] = [4, 4]
# h3.spellsKnown[FFSpellSystem.SpellInstance.BANE] = [4, 4]
# h1.spellsKnown[FFSpellSystem.SpellInstance.JUDGMENT] = [4, 4]
# h3.spellsKnown[FFSpellSystem.SpellInstance.SOFT] = [4, 4]
# h4.spellsKnown[FFSpellSystem.SpellInstance.BEACON] = [4, 4]
# h1.spellsKnown[FFSpellSystem.SpellInstance.DOOM] = [4, 4]
# h4.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]
#
# sleepStatus = FFStatusSystem.Sleep()
# paralysisStatus = FFStatusSystem.Paralysis()
# doomStatus = FFStatusSystem.Doom()
# stoneStatus = FFStatusSystem.Stone()
# silenceStatus = FFStatusSystem.Silence()
# confStatus = FFStatusSystem.Confusion()
# doomStatus.doomCount = 0
#
# h1.status = [doomStatus, silenceStatus, confStatus]
# h2.status = [silenceStatus, stoneStatus]
# h3.status = [silenceStatus]
# e1.status = [confStatus]
# e3.status = [confStatus]
# e3.maxHP = e3.currentHP = 100
# h1.spellsKnown[FFSpellSystem.SpellInstance.PURGE] = [2, 2]
# h2.spellsKnown[FFSpellSystem.SpellInstance.BEACON] = [1, 1]
# h3.spellsKnown[FFSpellSystem.SpellInstance.SILENCE] = [1, 1]
# # h1.experience += 100
# # FFLevelSystem.checkExperienceAndLevelUp(h1)
#
# armor = FFEquipmentSystem.Armor()
# armor.name = "Cool Armor"
#
# # armor.equipHero(h1)
# for __ in range(10):
#     FFBattleSystem.playerCurrentInventory.addItem(FFItemSystem.ItemInstance.PLAGUEBOMB)
#     FFBattleSystem.playerCurrentInventory.addItem(FFItemSystem.ItemInstance.BRIGHTHERB)
#     FFBattleSystem.playerCurrentInventory.addItem(FFItemSystem.ItemInstance.PARTYPOTION)
# FFItemSystem.ItemInstance.PLAGUEBOMB.targetParty = "Ally"
#
# e1.magicDef -= 500
# e2.magicDef -= 500
# e3.magicDef += 500
# # FFBattleSystem.startCombat(heroesList, enemiesList)
