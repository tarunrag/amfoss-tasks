use anyhow::Result;
use log::info;
use navnet_core::registry::StationRegistry;
// Import the missing function you found!
use navnet_core::migration::upgrade_legacy_snapshot;

fn main() -> Result<()> {
    env_logger::init();
    
    let mut registry = StationRegistry::new();
    info!("East Blue registry bootstrap initialized");

    // 1. Point to the YAML file located in the root of the repository
    // (Since we are in archives/east-blue, we go up two folders using ../../)
    let legacy_file_path = "../../legacy-stations.yml";
    
    // 2. Use the missing function to load and convert the YAML data
    let stations = upgrade_legacy_snapshot(legacy_file_path)?;

    // 3. Loop through all the recovered stations and add them to the registry
    for station in stations {
        registry.add_station(station)?;
    }

    info!("East Blue bootstrap completed with {} stations", registry.stations.len());
    
    Ok(())
}
