import FFBattleSystem
import FFSpellSystem

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
    hero.damage = max(1, hero.strength // 2)
    hero.defense = hero.armor
    hero.evasion = hero.agility
    hero.hitAmount = 1 + hero.hitRate // 32
    hero.fullName = hero.name

h1.spellsKnown[FFSpellSystem.SpellInstance.HASTE] = 1
h2.spellsKnown[FFSpellSystem.SpellInstance.STUN] = 1
h3.spellsKnown[FFSpellSystem.SpellInstance.SOFT] = 1
h4.spellsKnown[FFSpellSystem.SpellInstance.CURSE] = 1
h2.spellsKnown[FFSpellSystem.SpellInstance.DOOM] = 1
h3.spellsKnown[FFSpellSystem.SpellInstance.BANE] = 1

FFBattleSystem.controlCombatSystemLogic(heroes, enemiesList)