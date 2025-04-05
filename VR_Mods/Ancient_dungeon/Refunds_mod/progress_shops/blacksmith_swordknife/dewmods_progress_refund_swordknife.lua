local progressName = "progress_refund_swordknife"

local smithProgression = {}
-- BS Sword Knife
table.insert(smithProgression, {"progress_double_edged", 3})
table.insert(smithProgression, {"progress_fold_of_abberation", 1})
table.insert(smithProgression, {"progress_fold_of_obliteration", 1})
table.insert(smithProgression, {"progress_perfect_balance", 5})
table.insert(smithProgression, {"progress_weighted_pommel", 3})

-- rafis_dungeon_essentials - blacksmith_swordknife
table.insert(smithProgression, {"progress_avenge", 10})
table.insert(smithProgression, {"progress_debt", 10})
table.insert(smithProgression, {"progress_decintigration", 10})
table.insert(smithProgression, {"progress_demifiend_essence", 10})

--------------------
-- LOCAL FUNCTIONS
--------------------
local function refundSwordKnife()
    -- Load research unlock status
    for i = 1, #smithProgression do
        local progressName = smithProgression[i][1]
        local progressPrice = smithProgression[i][2]
        local isUnlocked = loadValue(progressName, false)

        -- Refund and re-lock
        if isUnlocked then
            -- Always allow refunds
            saveBool(progressName, false)

            player.BeastBlood = player.BeastBlood + progressPrice
        end
    end
end

-------------------
-- GLOBAL FUNCTIONS
-------------------
function onLoad()
	progress.name = "Buyer's Remorse"
	progress.desc = "Refund your sword & knife augments thanks to ancient consumer protections."
	progress.price = 0
end

function onBuy()
	refundSwordKnife()
end

function isBought()
    -- Always allow refunds
    return false
end