{
	"format_version": "1.12.0",
	"minecraft:geometry": [
		{
			"description": {
				"identifier": "geometry.narwal",
				"texture_width": 128,
				"texture_height": 128,
				"visible_bounds_width": 5,
				"visible_bounds_height": 2.5,
				"visible_bounds_offset": [0, 0.75, 0]
			},
			"bones": [
				{
					"name": "body",
					"pivot": [0, 0, -3],
					"cubes": [
						{"origin": [-4, 0.5, -2], "size": [8, 7, 12], "uv": [1, 28]}
					]
				},
				{
					"name": "head",
					"parent": "body",
					"pivot": [0, 0, -3],
					"cubes": [
						{
							"origin": [-4, 1, -9],
							"size": [8, 6, 7],
							"uv": {
								"north": {"uv": [79, 121], "uv_size": [8, 6]},
								"east": {"uv": [72, 121], "uv_size": [7, 6]},
								"south": {"uv": [79, 114.5], "uv_size": [8, 6]},
								"west": {"uv": [87, 121], "uv_size": [7, 6]},
								"up": {"uv": [79, 114], "uv_size": [8, 7]},
								"down": {"uv": [87, 121], "uv_size": [8, -7]}
							}
						}
					],
					"locators": {
						"lead": [0, 0, 0]
					}
				},
				{
					"name": "nose",
					"parent": "head",
					"pivot": [0, 0, -13],
					"cubes": [
						{"origin": [-0.7, 3.7, -24], "size": [1.1, 1.4, 15], "uv": [38, 45]}
					]
				},
				{
					"name": "tail",
					"parent": "body",
					"pivot": [0, 2.5, 11],
					"cubes": [
						{"origin": [-2, 0, 10], "size": [4, 5, 11], "uv": [42, 27]},
						{"origin": [-2.7, 1.1, 16], "size": [5.5, 4, 6], "uv": [17, 72]},
						{"origin": [-3, 1.1, 10], "size": [6, 5, 6], "uv": [16, 72]}
					]
				},
				{
					"name": "tail_fin",
					"parent": "tail",
					"pivot": [0, 2.5, 20],
					"cubes": [
						{"origin": [-5, 2, 21], "size": [10, 1, 6], "uv": [0, 47]}
					]
				},
				{
					"name": "back_fin",
					"parent": "body",
					"pivot": [0, 7, 2],
					"rotation": [-30, 0, 0],
					"cubes": [
						{"origin": [-1.5, 4.25, 2], "size": [3, 3, 8], "pivot": [0, 1, 1], "rotation": [30, 0, 0], "uv": [94, 13]}
					]
				},
				{
					"name": "left_fin",
					"parent": "body",
					"pivot": [3, 1, -1],
					"rotation": [0, -25, 20],
					"cubes": [
						{"origin": [3, 1, -2.5], "size": [8, 1, 4], "uv": [0, 54]}
					]
				},
				{
					"name": "right_fin",
					"parent": "body",
					"pivot": [-3, 1, -1],
					"rotation": [0, 25, -20],
					"cubes": [
						{"origin": [-11, 1, -2.5], "size": [8, 1, 4], "uv": [0, 54]}
					]
				}
			]
		}
	]
}
{
    "type": "minecraft:narwhal",
    "spawn_rules": {
        "biomes": [
            "minecraft:frozen_ocean",
            "minecraft:frozen_river",
            "minecraft:snowy_beach"
        ],
        "spawn_rate": 10,
        "group_size": [1, 3]
    },
    "sounds": {
        "ambient": "minecraft:entity.dolphin.ambient",
        "hurt": "minecraft:entity.dolphin.hurt",
        "death": "minecraft:entity.dolphin.death"
    },
    "attributes": {
        "health": 20,
        "movement_speed": 1.2,
        "damage_range": [9, 15.2]
    },
    "behavior": {
        "eats": ["minecraft:cod", "minecraft:salmon"],
        "aggressive_on_hit": true,
        "damage_on_aggression": 9
    },
    "drops": {
        "on_kill": {
            "effect": {
                "name": "minecraft:bad_omen",
                "duration": 12000
            }
        }
    },
    "model": {
        "texture": "texture (9).png",
        "swim_animation": {
            "file": "narwal.animation.json",
            "speed_multiplier": 0.5
        }
    }
	import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.level.Level;

public class NarwhalEntity extends Mob {

    private boolean isAggressive;

    public NarwhalEntity(EntityType<? extends Mob> entityType, Level world) {
        super(entityType, world);
        this.isAggressive = false;
    }

    @Override
    protected void registerGoals() {
        super.registerGoals();
        this.goalSelector.addGoal(1, new LookAtPlayerGoal(this, Player.class, 8.0f));
    }

    @Override
    public boolean hurt(LivingEntity source, float damage) {
        if (super.hurt(source, damage)) {
            if (!this.level.isClientSide) {
                if (source instanceof Player) {
                    this.isAggressive = true;
                    Player player = (Player) source;

                    // Spear attack on aggression
                    double damageDealt = this.random.nextDouble() * (7.6 - 4.5) + 4.5;
                    player.hurt(damageSource(this), (float) damageDealt);
                    this.playSound(SoundEvents.DOLPHIN_HURT, 1.0f, 1.0f);
                }
            }
            return true;
        }
        return false;
    }

    @Override
    public void die(DamageSource cause) {
        super.die(cause);

        if (cause.getEntity() instanceof Player) {
            Player player = (Player) cause.getEntity();

            // Apply Bad Omen effect on killing a narwhal
            player.addEffect(new MobEffectInstance(MobEffects.BAD_OMEN, 12000, 0)); // 10 minutes
            this.playSound(SoundEvents.DOLPHIN_DEATH, 1.0f, 1.0f);
        }
    }
}
{
    "type": "minecraft:narwhal",
    "spawn_rules": {
        "biomes": [
            "minecraft:frozen_ocean",
            "minecraft:frozen_river",
            "minecraft:snowy_beach"
        ],
        "spawn_rate": 10,
        "group_size": [1, 10]
    },
    "sounds": {
        "ambient": "minecraft:entity.dolphin.ambient",
        "hurt": "minecraft:entity.dolphin.hurt",
        "death": "minecraft:entity.dolphin.death"
    },
    "attributes": {
        "health": 20,
        "movement_speed": 1.2,
        "damage_range": [9, 15.2]
    },
    "behavior": {
        "eats": ["minecraft:cod", "minecraft:salmon"],
        "aggressive_on_hit": true,
        "damage_on_aggression": 9  // 4.5 hearts to 7.6 hearts
    },
    "drops": {
        "on_kill": {
            "effect": {
                "name": "minecraft:bad_omen",
                "duration": 12000
            }
        }
    }
}

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.biome.MobSpawnSettings;

public class ModEntityTypes {

    public static final EntityType<NarwhalEntity> NARWHAL = EntityType.Builder
            .of(NarwhalEntity::new, MobCategory.WATER_CREATURE)
            .sized(2.0F, 2.0F) // Set size of the narwhal (20-50x dolphin size)
            .build("narwhal");

    // Register attributes for the narwhal
    public static AttributeSupplier.Builder createNarwhalAttributes() {
        return AttributeSupplier.builder()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 1.2D)
                .add(Attributes.ATTACK_DAMAGE, 9.0D) // Base spear attack damage
                .add(Attributes.FOLLOW_RANGE, 16.0D); // For AI interactions
    }

    // Spawn settings (arctic biomes)
    public static void addNarwhalToBiomes() {
        MobSpawnSettings.SpawnerData narwhalSpawn = new MobSpawnSettings.SpawnerData(
                ModEntityTypes.NARWHAL, 10, 1, 3);
        BiomeLoadingEvent.getGeneration().addStructureStart(narwhalSpawn); // Adds to icy biomes
    }
}
{
  "format_version": 2,
  "header": {
    "name": "Narwhal Pack",
    "description": "A pack full of exciting narwhal-themed features and enhancements!",
    "uuid": "30c9c643-58c6-49ad-b746-bf3382305077", // Unique pack ID
    "version": [1, 0, 0], // Pack version
    "min_engine_version": [1, 20, 0] // Minimum version of the game required
  },
  "modules": [
    {
      "type": "resources",
      "uuid": "1a4b7705-5ac7-4771-8418-d219023d3745", // Unique module ID
      "version": [1, 0, 0]
    }
  ]
}
