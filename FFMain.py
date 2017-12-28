import FFBattleSystem
import FFSpellSystem
import FFLevelSystem

e1 = FFBattleSystem.Goblin()
e2 = FFBattleSystem.Goblin()
e3 = FFBattleSystem.Goblin()
enemiesList = [e1, e2, e3]
h1 = FFBattleSystem.Monk()
h2 = FFBattleSystem.BlackMage()
h3 = FFBattleSystem.WhiteMage()
h4 = FFBattleSystem.BlackMage()
heroes = [h1, h2, h3, h4]
for hero in heroes:
    hero.currentHP = hero.maxHP

h1.spellsKnown[FFSpellSystem.SpellInstance.HASTE] = [1, 1]
h2.spellsKnown[FFSpellSystem.SpellInstance.STUN] = [1, 1]
h2.spellsKnown[FFSpellSystem.SpellInstance.SOFT] = [1, 1]
h1.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]
h2.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]
h3.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]
h4.spellsKnown[FFSpellSystem.SpellInstance.CURSE] = [1, 1]
h2.spellsKnown[FFSpellSystem.SpellInstance.BANE] = [1, 1]
h3.spellsKnown[FFSpellSystem.SpellInstance.BANE] = [1, 1]
h4.spellsKnown[FFSpellSystem.SpellInstance.ARMAGEDDON] = [8, 8]

h1.status = ["Sleep", "Paralysis", "Doom"]
e3.maxHP = e3.currentHP = 100
h1.spellsKnown[FFSpellSystem.SpellInstance.PURGE] = [2, 2]
h2.spellsKnown[FFSpellSystem.SpellInstance.BEACON] = [1, 1]
h3.spellsKnown[FFSpellSystem.SpellInstance.SILENCE] = [1, 1]
# h1.experience += 100
# FFLevelSystem.checkExperienceAndLevelUp(h1)

print(h1.status)
FFBattleSystem.startCombat(heroes, enemiesList)
print(h1.status)
