# The Grand Line Restoration Initiative - Mission Log
1. Engineering Issues Identified

As I progressed through the archives, I encountered a mix of environment, logic, and configuration issues:

**Global Environment:** The Rust build process failed initially because the local Linux environment lacked a C compiler/linker (`cc`), preventing the final binaries from compiling.
**East Blue (Silent Failure & Hardcoded Logic):** The application compiled but exited immediately without standard output. Upon investigation, the startup script  **Reverse Mountain (Configuration Drift):** Integration tests were panicking due to a missing `assets` directory. The configuration file `application.toml` defined it, but the directory was missing from the filesystem, and the path resolution logic was looking in the wrong root folder.
 **Whiskey Peak (Lost History & Bypassed Logic):** The `legacy_mode` configuration flag was being parsed but entirely ignored by the system. The `effective_max_clients` logic was missing, and a previous engineer had lazily hardcoded `max_clients = 120` in the `.toml` file to bypass a unit test.
 **Alabasta (Dead Code & Unblocked Threads):** The Rust compiler emitted a `dead_code` warning because `data_dir` was defined in the `Coordinator` but never initialized. Furthermore, the `Service::start` function was a fake stub that exited immediately, preventing the application from running as a continuous network server.

2. Investigation Approach

To solve these issues without rewriting the codebase, I relied heavily on compiler output, environment variables, and testing traces:

  **Exposing Hidden Logs:** Since legacy apps often suppress `stdout`, I passed the `RUST_LOG=debug` (and `info`) environment variable to the `cargo run` commands. This exposed the hidden `env_logger` traces, proving when apps were intentionally exiting vs crashing.
  **Tracing Failing Tests:** In Reverse Mountain, I used `cargo test` to find the exact line causing the panic (`runtime.assets_dir.exists()`). I cross-referenced this with `runtime.rs` and realized it was joining paths relative to the `config/` directory, not the project root.
  **Git Archaeology & Deductive Reasoning:** In Whiskey Peak, I attempted to use `git log --follow -p src/config.rs` to find the deleted legacy logic. However, I discovered the entire Git history was wiped and squashed into a single commit (`GHOST IN THE TERMINAL`). I instead used deductive reasoning: by comparing the unit test's name (`defaults_to_100`) against its actual assertion (`120`), I deduced what the missing `legacy_mode` fallback logic was supposed to do.
  **Compiler-Driven Development:** In Alabasta, I used `cargo check` and investigated the yellow `#[warn(dead_code)]` trace to find the missing `data_dir` initialization block inside `coordinator.rs`. I then traced the application lifecycle from `main.rs` to `service.rs` to find why the thread wasn't blocking.

3. Fixes Applied
  **Linux Environment:** Cleared corrupted apt cache lists (`sudo rm -rf /var/lib/apt/lists/*`) and installed `build-essential` to provide the required C toolchain (`cc`) for Rust.
**East Blue:** Removed the hardcoded test station in `src/main.rs`. Imported the abandoned `navnet_core::migration::upgrade_legacy_snapshot` function, and wired the main loop to parse the root `../../legacy-stations.yml` file and populate the `StationRegistry`.
 **Reverse Mountain:** Created the missing assets folder in the correct location (`config/assets`) to satisfy the `config_dir.join()` path resolution logic found in `runtime.rs`.
  **Whiskey Peak:** Rewrote `effective_max_clients` to use `.unwrap_or_else()` to dynamically evaluate the `legacy_mode` flag, returning 120 if true and 100 if false. Removed the hardcoded override from `application.toml`.
 **Alabasta:** 
    1. Added missing directory creation logic (`fs::create_dir_all`) for `data_dir` inside `Coordinator::initialize`.
    2. Replaced the empty `Service::start` stub with an infinite `loop { std::thread::park(); }` to safely block the main thread and keep the network service alive without consuming CPU cycles.

4. Rust, Git, and Linux Concepts Involved

  **Rust:** 
    *   Handling `Result` types and error propagation using the `?` operator.
    *   Iterating over vectors with `for` loops.
    *   File system path resolution (`std::path::Path`) and joining relative paths.
    *   Closures and Option handling (`.unwrap_or_else(|| { ... })`).
    *   Thread management and safe blocking (`std::thread::park`).
    *   Resolving compiler warnings (`dead_code`).
    **Git:** 
    *   Understanding Git tree states, squashed commits, and attempting to track file history (`git diff`, `git log --follow`).
    *   Managing ignored files vs tracked files (e.g., why empty directories disappear in Git, causing config drift).
  **Linux:** 
    *   Managing package caches (`apt`).
    *   Injecting environment variables at runtime (`RUST_LOG=info cargo run`).
