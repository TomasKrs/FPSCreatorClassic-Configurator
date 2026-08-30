# FPSCreatorClassic-Configurator

An setup.ini configurator and optimizer for FPS Creator Classic. Designed to maximize performance, tweak lighting bake quality, prevent 2GB RAM crashes, and optimize graphic settings for any hardware — from low-end Intel HD integrated GPUs to high-end dedicated gaming graphics cards.

<img width="915" height="674" alt="obrázok" src="https://github.com/user-attachments/assets/d20f6985-bf67-477f-b7df-c51d7a019b8b" />


## **What do you need**

FPS Creator Classic updated to version 1.20
BlackIceMode v12

I didnt test it on Steam release and BlackIceModAdvanced. It wouldnt work there (because of other parameters in setup.ini).

## **🚀 Features**

🖥️ Dual Interface: Runs in a modern GUI (Tkinter Dark Mode) or a lightweight Console / CLI mode.

🌐 Bilingual (EN / SK): Instant toggling between English and Slovak languages.

⚡ 5 Pre-configured Hardware Profiles: One-click presets tailored to specific GPU capabilities.

🎛️ Granular Tweak Panel: Tweak individual parameters (Shaders, Dynamic Shadows, Post-Processing, Lightmap Quality, Texture Division, AI Radius).

🛡️ Safety & Automatic Backups: Automatically creates timestamped backups (setup_backup_YYYYMMDD_HHMMSS.ini) before applying any modifications.

🔓 2GB RAM Limit Bypass (systemmemorycapoff): Unlocks full system RAM usage during lightmap baking to eliminate editor crashes on modern 64-bit systems.

📦 Standalone Executable: Ready to be compiled into a single .exe file without requiring Python on target machines.

🎮 Hardware Profiles Breakdown


## **Profile**

⚡ Extreme Performance
Intel HD 2000–4000, GMA, Old Laptops
Disables shaders/particles, 25% texture resolution (dividetexturesize=2), lowest bake quality.

⚙️ Balanced Integrated
Intel UHD 620/630, Iris Xe, AMD Vega
Enables gun/entity shaders, disables dynamic shadows, 50% textures (dividetexturesize=1).

🎨 High Quality
GTX 750 Ti / 960 / 1050, RX 560+
Full texture resolution (100%), full scene shaders, post-processing enabled, 1024px lightmaps.

🔥 Ultra Cinematic
GTX 1060+, RTX Series, RX 6000+
All visual effects maxed out, real-time dynamic shadows, 2K lightmaps (lightmaptexsize=2048).

🕹️ Retro 90s Pixel
Any PC (Aesthetic Mode)
Extreme 12.5% texture compression (dividetexturesize=4) for authentic Quake/Doom 90s graphics.



## **📥 Installation & Running**

Just copy FPSCreator_Configurator.exe to your FPS Creator Classic dir and run it.
