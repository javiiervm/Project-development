local progressName = "progress_refund_insight"

-- progression[][] = {name, cost}
local acoProgression = {}
table.insert(acoProgression, {"progress_business_senseless", 50})
table.insert(acoProgression, {"progress_devilish_deals", 40})
table.insert(acoProgression, {"progress_dilemmatic_pedestals", 60})
table.insert(acoProgression, {"progress_hidden_passages", 20})
table.insert(acoProgression, {"progress_honeypot", 100})
table.insert(acoProgression, {"progress_i_have_a_system", 30})
table.insert(acoProgression, {"progress_marvellous_marks", 50})
table.insert(acoProgression, {"progress_shiney_slimey", 125})
table.insert(acoProgression, {"progress_smorgasbord", 80})
table.insert(acoProgression, {"progress_super_size_me", 50})
table.insert(acoProgression, {"progress_the_boss_stash", 40})

-- rafis_dungeon_essentials - acolyte
table.insert(acoProgression, {"progress_bloody_coffee", 50})
table.insert(acoProgression, {"progress_celestial", 100})
table.insert(acoProgression, {"progress_constant_growth", 75})
table.insert(acoProgression, {"progress_deadlye", 100})
table.insert(acoProgression, {"progress_gaea_rage", 105})
table.insert(acoProgression, {"progress_haggling", 125})
table.insert(acoProgression, {"progress_pills", 150})
table.insert(acoProgression, {"progress_thoms_intuition", 75})

-- rafis_generation_amplifiers - acolyte
table.insert(acoProgression, {"progress_cond", 0})
table.insert(acoProgression, {"progress_depths", 0})
table.insert(acoProgression, {"progress_lab", 0})

-- TerrariaMini - acolyte
table.insert(acoProgression, {"shimmer", 50})

-- DungeonTactica - acolyte
table.insert(acoProgression, {"dungeon_tactica_map", 100})
table.insert(acoProgression, {"dungeon_tactica_regen", 200})
table.insert(acoProgression, {"dungeon_tactica_randeffect", 1})
table.insert(acoProgression, {"dungeon_tactica_boss_pedestals", 200})
table.insert(acoProgression, {"dungeon_tactica_hunters_eye", 75})

-- Expansion - acolyte
table.insert(acoProgression, {"progress_babymode", 5})
table.insert(acoProgression, {"progress_auto_charger", 100})
table.insert(acoProgression, {"progress_challenge_nullifier", 100})
table.insert(acoProgression, {"progress_compact_clusters", 100})
table.insert(acoProgression, {"progress_crit_eye", 65})
table.insert(acoProgression, {"progress_darkness", 1})
table.insert(acoProgression, {"progress_empty_marketplace", 150})
table.insert(acoProgression, {"progress_explorer", 5})
table.insert(acoProgression, {"progress_focus", 180})
table.insert(acoProgression, {"progress_momentum", 150})
table.insert(acoProgression, {"progress_raging_pedestals", 60})
table.insert(acoProgression, {"progress_wisp_companion", 25})

-- Dungeon+ - acolyte
table.insert(acoProgression, {"progress_fog_who", 15})
table.insert(acoProgression, {"progress_return_to_sender", 15})
table.insert(acoProgression, {"progress_ironfist", 10})
table.insert(acoProgression, {"progress_gambling", 15})
table.insert(acoProgression, {"progress_merchants_casino", 15})
table.insert(acoProgression, {"progress_powerful_fist", 15})

-- Dungeon++ - acolyte
table.insert(acoProgression, {"progress_crystal_dng++_lightbulb", 50})
table.insert(acoProgression, {"progress_tuxx_dng++_always_bring_protection", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_always_bring_protection_three", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_always_bring_protection_two", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_fog_who", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_food_frenzy", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_gambling", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_iron_fist", 10})
table.insert(acoProgression, {"progress_tuxx_dng++_merchants_casino", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_powerful_fist", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_return_to_sender", 15})
table.insert(acoProgression, {"progress_tuxx_dng++_resilience", 120})

-- Battle+ - acolyte
table.insert(acoProgression, {"progress_firecracker", 150})
table.insert(acoProgression, {"progress_guardian_wisp", 150})
table.insert(acoProgression, {"progress_no_gravity", 150})
table.insert(acoProgression, {"progress_projectile_seek", 150})
table.insert(acoProgression, {"progress_projectile_speed", 150})
table.insert(acoProgression, {"progress_pyro", 150})

-- Battle+ Lite - acolyte

-- PENDING TO ADD AUTOMATIC SYSTEM


--------------------
-- LOCAL FUNCTIONS
--------------------
local function refundResearch()
    -- Load research unlock status
    for i = 1, #acoProgression do
        local progressName = acoProgression[i][1]
        local progressPrice = acoProgression[i][2]
        local unlocked = loadValue(progressName, false)

        -- Refund insight and re-lock
        if unlocked then
            saveBool(progressName, false)
            player.Insight = player.Insight + progressPrice
        end
    end

    -- Check if the player has bought "Buyer's Remorse" and remove it
    local boughtBuyersRemorse = loadValue("progress_refund_insight", false)
    if boughtBuyersRemorse then
        saveBool("progress_refund_insight", false)
        player.Insight = player.Insight + progress.price
    end
end

-------------------
-- GLOBAL FUNCTIONS
-------------------
function onLoad()
    progress.name = "Buyer's Remorse"
    progress.desc = "<i>Refund your insight purchases thanks to ancient consumer protections.</i>"
    progress.price = 0
    -- progress.category = "Misc"

    -- Check if the player has bought "Buyer's Remorse" and remove it
    local boughtBuyersRemorse = loadValue("progress_refund_insight", false)
    if boughtBuyersRemorse then
        saveBool("progress_refund_insight", false)
        player.Insight = player.Insight + progress.price
    end
end

function onBuy()
	refundResearch()
end

function isBought()
    return false
end