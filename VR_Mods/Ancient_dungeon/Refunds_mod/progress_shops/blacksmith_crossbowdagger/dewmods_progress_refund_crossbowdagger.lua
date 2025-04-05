local progressName = "progress_refund_crossbowdagger"

local smithProgression = {}
-- BS Crossbow Dagger
table.insert(smithProgression, {"progress_caustic_alloy", 3})
table.insert(smithProgression, {"progress_pressurized_capsule", 3})
table.insert(smithProgression, {"progress_reactive_polarization", 5})
table.insert(smithProgression, {"progress_tensioning_winch", 3})
table.insert(smithProgression, {"progress_tethered_bolt", 1})

-- rafis_dungeon_essentials - blacksmith_crossbowdagger
table.insert(smithProgression, {"progress_ideal_conc", 10})
table.insert(smithProgression, {"progress_impalers_glory", 10})
table.insert(smithProgression, {"progress_jack_gloves", 5})
table.insert(smithProgression, {"progress_lucifer_bullet", 10})

--------------------
-- LOCAL FUNCTIONS
--------------------
local function refundCrossbowDagger()
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
	progress.desc = "Refund your crossbow & dagger augments thanks to ancient consumer protections."
	progress.price = 0
end

function onBuy()
	refundCrossbowDagger()
end

function isBought()
    -- Always allow refunds
    return false
end