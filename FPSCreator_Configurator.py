import os
import sys
import re
import shutil
import datetime
from typing import Dict, List, Tuple, Optional

# Attempt to import tkinter for GUI mode
GUI_AVAILABLE = True
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
except ImportError:
    GUI_AVAILABLE = False

INI_FILE_NAME = "setup.ini"

TRANSLATIONS = {
    "en": {
        "title": "🎮 FPS Creator Classic - Setup Configurator PRO",
        "header_title": "🎮 FPS Creator Classic - Configurator",
        "select_file": "📁 Select setup.ini",
        "lang_btn": "🇸🇰 Slovenčina",
        "status_file": "File:",
        "tab_profiles": "🚀 Quick Profiles (GPU)",
        "tab_custom": "🎛️ Advanced Settings",
        "tab_editor": "📄 INI Preview & Backups",
        "profiles_intro": "Select a performance profile based on your graphics card capabilities:",
        "apply_profile": "Apply Profile",
        "custom_gfx_header": " 🎨 Graphics, Effects & VRAM (GAMERUN) ",
        "tex_div_label": "Texture Quality in VRAM (dividetexturesize):",
        "tex_opt_0": "0 - Full Resolution (100% VRAM)",
        "tex_opt_1": "1 - Medium Quality (50% VRAM)",
        "tex_opt_2": "2 - Quarter Quality (25% VRAM - Recommended for Intel HD)",
        "tex_opt_4": "4 - Retro 90s Pixelated (12.5% VRAM)",
        "shadows_cb": "Real-time Dynamic Shadows (dynamicshadows - High GPU Load)",
        "postproc_cb": "Post-Processing Effects (postprocessing - Bloom, DoF, Motion Blur)",
        "shaders_cb": "Enable DirectX Pixel/Vertex Shaders (useeffects)",
        "particles_cb": "Disable Smoke/Particle Effects (disableparticles - Boosts CPU FPS)",
        "custom_light_header": " 💡 Lightmapping & Baking Quality (GAMEMAKE) ",
        "ltex_label": "Lightmap Resolution (lightmaptexsize):",
        "ltex_opt_256": "256 - Fast / Low Quality",
        "ltex_opt_512": "512 - Balanced",
        "ltex_opt_1024": "1024 - High Quality",
        "ltex_opt_2048": "2048 - Ultra Crisp Lights",
        "lqual_label": "Lightmap Quality (lightmapquality):",
        "lqual_hint": "(Tip: 5=Fast Preview, 20=Standard, 50=Final Bake)",
        "ram_cap_cb": "Disable 2GB RAM Limit (systemmemorycapoff - Prevents crashes during light baking!)",
        "custom_engine_header": " ⚙️ AI & Engine Optimization ",
        "airadius_label": "AI Radius Calculation (airadius in tiles):",
        "airadius_hint": "(Lower value e.g. 10 = less CPU strain)",
        "save_custom_btn": "💾 Save Custom Settings to setup.ini",
        "reload_preview": "🔄 Refresh Preview",
        "create_backup_btn": "📦 Create Backup Now",
        "save_editor_btn": "💾 Save Direct Edits from Editor",
        "backup_success": "Backup Created",
        "backup_success_msg": "Backup saved successfully to:\n",
        "backup_error": "Failed to create backup.",
        "confirm_profile_title": "Confirm Profile",
        "confirm_profile_msg": "Do you want to apply the following profile?\n",
        "success": "Success",
        "profile_applied": "Profile applied successfully!",
        "save_success": "Settings saved successfully to setup.ini!",
        "error": "Error",
        "file_not_found": "File setup.ini was not found!",
        "write_error": "Failed to write updates to setup.ini.",
        "cli_title": "    🎮 FPS CREATOR CLASSIC - SETUP.INI CONFIGURATOR (CLI)      ",
        "cli_current": "Current File:",
        "cli_available": "Available Pre-configured Profiles:",
        "cli_option_m": " [M] 🎛️ Manual tweak parameters",
        "cli_option_b": " [B] 📦 Create backup of setup.ini",
        "cli_option_l": " [L] 🌐 Switch Language (SK/EN)",
        "cli_option_0": " [0] 🚪 Exit Configurator",
        "cli_prompt": "Select an option: "
    },
    "sk": {
        "title": "🎮 FPS Creator Classic - Konfigurátor Nastavení PRO",
        "header_title": "🎮 FPS Creator Classic - Konfigurátor",
        "select_file": "📁 Vybrať setup.ini",
        "lang_btn": "🇬🇧 English",
        "status_file": "Súbor:",
        "tab_profiles": "🚀 Rýchle Profily (GPU)",
        "tab_custom": "🎛️ Detailné Nastavenia",
        "tab_editor": "📄 Náhľad INI & Zálohy",
        "profiles_intro": "Vyberte profil podľa vašej grafickej karty a požadovaného výkonu:",
        "apply_profile": "Aplikovať profil",
        "custom_gfx_header": " 🎨 Grafika, Efekty a VRAM (GAMERUN) ",
        "tex_div_label": "Kvalita textúr v VRAM (dividetexturesize):",
        "tex_opt_0": "0 - Plná kvalita (100% VRAM)",
        "tex_opt_1": "1 - Stredná kvalita (50% VRAM)",
        "tex_opt_2": "2 - Štvrtinová kvalita (25% VRAM - Odporúčané pre Intel HD)",
        "tex_opt_4": "4 - Retro 90s Pixelated (12.5% VRAM)",
        "shadows_cb": "Dynamické tiene v reálnom čase (dynamicshadows - Veľmi náročné)",
        "postproc_cb": "Post-Processing efekty (postprocessing - Bloom, DoF, Motion Blur)",
        "shaders_cb": "Povoliť DirectX pixel/vertex šejdery (useeffects)",
        "particles_cb": "Vypnúť častice/dym/ohňové efekty (disableparticles - Zvýši FPS na CPU)",
        "custom_light_header": " 💡 Lightmapping & Pečenie Svetiel (GAMEMAKE) ",
        "ltex_label": "Rozlíšenie Lightmapy (lightmaptexsize):",
        "ltex_opt_256": "256 - Rýchle / Nízka kvalita",
        "ltex_opt_512": "512 - Vyvážené",
        "ltex_opt_1024": "1024 - Vysoká kvalita",
        "ltex_opt_2048": "2048 - Ultra Ostré svetlá",
        "lqual_label": "Kvalita Pečenia Svetla (lightmapquality):",
        "lqual_hint": "(Tip: 5=Rýchly náhľad, 20=Štandard, 50=Finálny Build)",
        "ram_cap_cb": "Vypnúť 2GB RAM Limit (systemmemorycapoff - Zabraňuje padaniu pri výpočte svetiel!)",
        "custom_engine_header": " ⚙️ AI a Optimalizácia Motora ",
        "airadius_label": "Rádius AI Výpočtov (airadius v dlaždiciach):",
        "airadius_hint": "(Nižšie číslo napr. 10 = menej vyťaženia CPU)",
        "save_custom_btn": "💾 Uložiť vlastné nastavenia do setup.ini",
        "reload_preview": "🔄 Obnoviť náhľad",
        "create_backup_btn": "📦 Vytvoriť zálohu teraz",
        "save_editor_btn": "💾 Uložiť priame zmeny z textového editora",
        "backup_success": "Záloha Vytvorená",
        "backup_success_msg": "Záloha bola úspešne uložená do:\n",
        "backup_error": "Zálohu sa nepodarilo vytvoriť.",
        "confirm_profile_title": "Potvrdiť profil",
        "confirm_profile_msg": "Naozaj chcete aplikovať nasledujúci profil?\n",
        "success": "Úspech",
        "profile_applied": "Profil bol úspešne aplikovaný!",
        "save_success": "Nastavenia boli úspešne uložené do setup.ini!",
        "error": "Chyba",
        "file_not_found": "Súbor setup.ini nebol nájdený!",
        "write_error": "Nepodarilo sa zapísať zmeny do setup.ini.",
        "cli_title": "    🎮 FPS CREATOR CLASSIC - SETUP.INI CONFIGURATOR (CLI)      ",
        "cli_current": "Aktuálny súbor:",
        "cli_available": "Dostupné prednastavené profily:",
        "cli_option_m": " [M] 🎛️ Ručné úpravy vybraných parametrov",
        "cli_option_b": " [B] 📦 Vytvoriť zálohu súboru setup.ini",
        "cli_option_l": " [L] 🌐 Zmeniť Jazyk (SK/EN)",
        "cli_option_0": " [0] 🚪 Ukončiť program",
        "cli_prompt": "Vyberte možnosť: "
    }
}

PROFILES: Dict[str, dict] = {
    "1": {
        "id": "potato",
        "badge": "LOW-END / INTEL HD",
        "badge_color": "#e74c3c",
        "name": {
            "en": "⚡ Extreme Performance / Intel HD (Potato PC)",
            "sk": "⚡ Extrémny Výkon / Intel HD (Slabé PC)"
        },
        "gpu_hint": {
            "en": "Suitable for: Old laptops, Intel HD 2000/3000/4000, GMA graphics, VRAM < 512MB.",
            "sk": "Vhodné pre: Staré notebooky, Intel HD 2000/3000/4000, GMA grafiky, VRAM < 512MB."
        },
        "desc": {
            "en": "Maximum visual stripping for smooth FPS on the weakest hardware. Disables shaders and reduces textures to 25%.",
            "sk": "Maximálne orezanie vizuálnych efektov pre plynulý chod. Vypína šejdery, časť častíc a zmenšuje textúry na 25%."
        },
        "data": {
            "GAMERUN": {
                "dynamiclighting": "1", "dynamicshadows": "0", "useeffects": "0",
                "useeffectsonguns": "0", "useeffectsonscene": "0", "useeffectsonentities": "0",
                "dividetexturesize": "2", "newblossershaders": "0", "postprocessing": "0",
                "skyboxshader": "0", "darkaion": "1", "newlight": "0", "disableparticles": "1",
                "airadius": "12", "hsrmode": "2", "optimizemode": "1"
            },
            "GAMEMAKE": {
                "lightmapping": "1", "lightmapshadows": "0", "lightmaptexsize": "256",
                "lightmapquality": "5", "lightmapblurmode": "1", "systemmemorycapoff": "1",
                "extracollisionbuilddisabled": "1"
            }
        }
    },
    "2": {
        "id": "integrated",
        "badge": "MID INTEGRATED",
        "badge_color": "#e67e22",
        "name": {
            "en": "⚙️ Balanced Integrated (Intel UHD / Iris Xe / Vega)",
            "sk": "⚙️ Vyvážené Integrované (Intel UHD / Iris Xe / Vega)"
        },
        "gpu_hint": {
            "en": "Suitable for: Intel Iris Xe, Intel UHD 620/630, AMD Radeon Vega 3/8/11, GT 730.",
            "sk": "Vhodné pre: Intel Iris Xe, Intel UHD 620/630, AMD Radeon Vega 3/8/11, GT 730."
        },
        "desc": {
            "en": "Great compromise for modern laptop integrated chips. Enables weapon & entity shaders, disables dynamic shadows.",
            "sk": "Skvelý kompromis pre moderné notebookové čipy. Zapína efekty na zbraniach, vypína náročné tiene."
        },
        "data": {
            "GAMERUN": {
                "dynamiclighting": "1", "dynamicshadows": "0", "useeffects": "1",
                "useeffectsonguns": "1", "useeffectsonscene": "0", "useeffectsonentities": "1",
                "dividetexturesize": "1", "newblossershaders": "0", "postprocessing": "0",
                "skyboxshader": "0", "darkaion": "1", "newlight": "1", "disableparticles": "0",
                "airadius": "18", "hsrmode": "2", "optimizemode": "1"
            },
            "GAMEMAKE": {
                "lightmapping": "1", "lightmapshadows": "1", "lightmaptexsize": "512",
                "lightmapquality": "15", "lightmapblurmode": "1", "systemmemorycapoff": "1",
                "extracollisionbuilddisabled": "1"
            }
        }
    },
    "3": {
        "id": "dedicated",
        "badge": "DEDICATED GPU",
        "badge_color": "#2ecc71",
        "name": {
            "en": "🎨 High Quality (Dedicated GPUs - GTX 750 / RX 560+)",
            "sk": "🎨 Vysoká Kvalita (Dedikované karty - GTX 750 / RX 560+)"
        },
        "gpu_hint": {
            "en": "Suitable for: NVIDIA GTX 750 Ti / 960 / 1050, AMD Radeon RX 460 / 560 and better.",
            "sk": "Vhodné pre: NVIDIA GTX 750 Ti / 960 / 1050, AMD Radeon RX 460 / 560 a lepšie."
        },
        "desc": {
            "en": "Beautiful visual experience. Full resolution textures, full scene shaders, post-processing enabled.",
            "sk": "Krásny visual. Plné textúry, šejdery pre celú scénu, post-processing a kvalitnejší lightmap bake."
        },
        "data": {
            "GAMERUN": {
                "dynamiclighting": "1", "dynamicshadows": "0", "useeffects": "1",
                "useeffectsonguns": "1", "useeffectsonscene": "1", "useeffectsonentities": "1",
                "dividetexturesize": "0", "newblossershaders": "1", "postprocessing": "1",
                "skyboxshader": "1", "darkaion": "1", "newlight": "1", "disableparticles": "0",
                "airadius": "25", "hsrmode": "2", "optimizemode": "1"
            },
            "GAMEMAKE": {
                "lightmapping": "1", "lightmapshadows": "1", "lightmaptexsize": "1024",
                "lightmapquality": "35", "lightmapblurmode": "1", "systemmemorycapoff": "1",
                "extracollisionbuilddisabled": "1"
            }
        }
    },
    "4": {
        "id": "ultra",
        "badge": "ULTRA GAMING",
        "badge_color": "#9b59b6",
        "name": {
            "en": "🔥 Ultra Cinematic (Modern Gaming PC - RTX / RX 6000+)",
            "sk": "🔥 Ultra Kinematický (Herné PC - RTX / RX 6000+)"
        },
        "gpu_hint": {
            "en": "Suitable for: NVIDIA GTX 1060 / RTX 2060/3060/4060, AMD RX 6600+.",
            "sk": "Vhodné pre: NVIDIA GTX 1060 / RTX 2060/3060/4060, AMD RX 6600+."
        },
        "desc": {
            "en": "All visual effects set to maximum! Dynamic realtime shadows, full post-processing, 2K lightmaps.",
            "sk": "Všetky efekty na maximum! Dynamické tiene v reálnom čase, plný post-processing, 2K lightmapy."
        },
        "data": {
            "GAMERUN": {
                "dynamiclighting": "1", "dynamicshadows": "1", "useeffects": "1",
                "useeffectsonguns": "1", "useeffectsonscene": "1", "useeffectsonentities": "1",
                "dividetexturesize": "0", "newblossershaders": "1", "postprocessing": "1",
                "skyboxshader": "1", "darkaion": "1", "newlight": "1", "disableparticles": "0",
                "airadius": "30", "hsrmode": "2", "optimizemode": "1"
            },
            "GAMEMAKE": {
                "lightmapping": "1", "lightmapshadows": "1", "lightmaptexsize": "2048",
                "lightmapquality": "50", "lightmapblurmode": "2", "systemmemorycapoff": "1",
                "extracollisionbuilddisabled": "0"
            }
        }
    },
    "5": {
        "id": "retro",
        "badge": "RETRO STYLE",
        "badge_color": "#f1c40f",
        "name": {
            "en": "🕹️ Retro 90s Pixel Style (Quake / Doom Atmosphere)",
            "sk": "🕹️ Retro 90s Pixel Štýl (Atmosphere Quake / Doom)"
        },
        "gpu_hint": {
            "en": "Suitable for: Any hardware (Retro aesthetic with pixelated textures).",
            "sk": "Vhodné pre: Akýkoľvek hardvér (Retro estetika s pixelovanými textúrami)."
        },
        "desc": {
            "en": "Special profile enabling severe texture compression (dividetexturesize=4) for retro 90s pixelation.",
            "sk": "Špeciálny profil s silným orezaním textúr (dividetexturesize=4) pre pixelovaný retro 90s štýl."
        },
        "data": {
            "GAMERUN": {
                "dynamiclighting": "1", "dynamicshadows": "0", "useeffects": "0",
                "useeffectsonguns": "0", "useeffectsonscene": "0", "useeffectsonentities": "0",
                "dividetexturesize": "4", "newblossershaders": "0", "postprocessing": "0",
                "skyboxshader": "0", "disableparticles": "0", "airadius": "15"
            },
            "GAMEMAKE": {
                "lightmapping": "1", "lightmapshadows": "0", "lightmaptexsize": "256",
                "lightmapquality": "10", "systemmemorycapoff": "1"
            }
        }
    }
}

class SetupIniManager:
    """Manager for safe reading, writing, and backing up setup.ini."""
    def __init__(self, filepath: str = INI_FILE_NAME):
        self.filepath = os.path.abspath(filepath)

    def exists(self) -> bool:
        return os.path.exists(self.filepath)

    def create_backup(self) -> Optional[str]:
        if not self.exists():
            return None
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"setup_backup_{timestamp}.ini"
        backup_path = os.path.join(os.path.dirname(self.filepath), backup_name)
        try:
            shutil.copy2(self.filepath, backup_path)
            return backup_path
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None

    def read_lines(self) -> List[str]:
        if not self.exists():
            return []
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.readlines()

    def write_lines(self, lines: List[str]) -> bool:
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        except Exception as e:
            print(f"Error writing INI file: {e}")
            return False

    def get_all_settings(self) -> Dict[str, Dict[str, str]]:
        lines = self.read_lines()
        data = {}
        current_section = "GLOBAL"
        for line in lines:
            clean = line.strip()
            if not clean or clean.startswith(';') or clean.startswith('#'):
                continue
            if clean.startswith('[') and clean.endswith(']'):
                current_section = clean[1:-1].strip().upper()
                if current_section not in data:
                    data[current_section] = {}
            elif '=' in clean:
                parts = clean.split('=', 1)
                key = parts[0].strip()
                val = parts[1].strip()
                if current_section not in data:
                    data[current_section] = {}
                data[current_section][key] = val
        return data

    def update_key_in_lines(self, lines: List[str], section: str, key: str, new_value: str) -> List[str]:
        current_sec = ""
        new_lines = []
        for line in lines:
            clean = line.strip()
            if clean.startswith('[') and clean.endswith(']'):
                current_sec = clean[1:-1].strip().upper()
                new_lines.append(line)
            elif '=' in clean and current_sec == section.upper():
                parts = line.split('=', 1)
                k = parts[0].strip()
                if k.lower() == key.lower():
                    prefix = line[:line.find('=')]
                    new_lines.append(f"{prefix}={new_value}\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        return new_lines

    def apply_dict_updates(self, updates: Dict[str, Dict[str, str]], auto_backup: bool = True) -> bool:
        if auto_backup:
            self.create_backup()
        lines = self.read_lines()
        if not lines:
            return False
        for section, kv_pairs in updates.items():
            for key, val in kv_pairs.items():
                lines = self.update_key_in_lines(lines, section, key, str(val))
        return self.write_lines(lines)

class ConfiguratorGUI:
    """Tkinter Graphical Interface with Language Switching & Dark Theme."""
    def __init__(self, root: tk.Tk, manager: SetupIniManager):
        self.root = root
        self.manager = manager
        self.lang = "en"  # Default language: English ("en") or Slovak ("sk")

        self.root.title(TRANSLATIONS[self.lang]["title"])
        self.root.geometry("920x700")
        self.root.minsize(850, 620)

        # Dark Theme Palette
        self.colors = {
            "bg": "#1e1e2e",
            "card_bg": "#252538",
            "card_border": "#313244",
            "fg": "#cdd6f4",
            "accent": "#89b4fa",
            "accent_hover": "#b4befe",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "danger": "#f38ba8",
            "subtext": "#a6adc8"
        }

        self.setup_styles()
        self.create_widgets()
        self.load_current_values()

    def t(self, key: str) -> str:
        """Helper to retrieve translated string for current language."""
        return TRANSLATIONS[self.lang].get(key, key)

    def toggle_language(self):
        """Switch language between English and Slovak dynamically."""
        self.lang = "sk" if self.lang == "en" else "en"
        self.root.title(self.t("title"))
        self.lang_btn.config(text=self.t("lang_btn"))
        self.header_title.config(text=self.t("header_title"))
        self.path_btn.config(text=self.t("select_file"))
        self.status_var.set(f"{self.t('status_file')} {self.manager.filepath}")

        # Update Tab Titles
        self.notebook.tab(self.tab_profiles, text=self.t("tab_profiles"))
        self.notebook.tab(self.tab_custom, text=self.t("tab_custom"))
        self.notebook.tab(self.tab_editor, text=self.t("tab_editor"))

        # Re-build profiles & update combo options
        self.rebuild_profiles_tab()
        self.update_custom_tab_translations()
        self.update_editor_tab_translations()

    def setup_styles(self):
        self.root.configure(bg=self.colors["bg"])
        style = ttk.Style()
        style.theme_use('default')

        style.configure(".", background=self.colors["bg"], foreground=self.colors["fg"], font=("Segoe UI", 10))
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors["card_bg"], foreground=self.colors["fg"], 
                        padding=[14, 8], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.colors["accent"])], 
                  foreground=[("selected", "#11111b")])

        style.configure("TLabelframe", background=self.colors["card_bg"], foreground=self.colors["accent"],
                        borderColor=self.colors["card_border"], borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background=self.colors["card_bg"], foreground=self.colors["accent"],
                        font=("Segoe UI", 11, "bold"))

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.colors["card_bg"], height=70)
        header_frame.pack(fill="x", side="top", padx=0, pady=0)

        self.header_title = tk.Label(header_frame, text=self.t("header_title"),
                                     font=("Segoe UI", 16, "bold"), bg=self.colors["card_bg"], fg=self.colors["accent"])
        self.header_title.pack(side="left", padx=20, pady=15)

        # Language Switcher Button
        self.lang_btn = tk.Button(header_frame, text=self.t("lang_btn"), bg=self.colors["accent"], fg="#11111b",
                                  font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=6, command=self.toggle_language)
        self.lang_btn.pack(side="right", padx=(5, 20), pady=15)

        # File Chooser Button
        self.path_btn = tk.Button(header_frame, text=self.t("select_file"), bg=self.colors["bg"], fg=self.colors["fg"],
                                  activebackground=self.colors["accent"], activeforeground="#11111b",
                                  bd=1, relief="solid", padx=10, pady=5, command=self.browse_ini_file)
        self.path_btn.pack(side="right", padx=5, pady=15)

        # Status bar
        self.status_var = tk.StringVar(value=f"{self.t('status_file')} {self.manager.filepath}")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w",
                              bg=self.colors["card_bg"], fg=self.colors["subtext"], font=("Segoe UI", 9))
        status_bar.pack(side="bottom", fill="x")

        # Main Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Tabs
        self.tab_profiles = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_profiles, text=self.t("tab_profiles"))
        self.build_profiles_tab()

        self.tab_custom = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_custom, text=self.t("tab_custom"))
        self.build_custom_tab()

        self.tab_editor = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_editor, text=self.t("tab_editor"))
        self.build_editor_tab()

    def build_profiles_tab(self):
        self.profiles_canvas = tk.Canvas(self.tab_profiles, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_profiles, orient="vertical", command=self.profiles_canvas.yview)
        self.profiles_scroll_frame = tk.Frame(self.profiles_canvas, bg=self.colors["bg"])

        self.profiles_scroll_frame.bind("<Configure>", lambda e: self.profiles_canvas.configure(scrollregion=self.profiles_canvas.bbox("all")))
        self.profiles_canvas.create_window((0, 0), window=self.profiles_scroll_frame, anchor="nw")
        self.profiles_canvas.configure(yscrollcommand=scrollbar.set)

        self.profiles_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        self.rebuild_profiles_tab()

    def rebuild_profiles_tab(self):
        for widget in self.profiles_scroll_frame.winfo_children():
            widget.destroy()

        intro_lbl = tk.Label(self.profiles_scroll_frame, text=self.t("profiles_intro"),
                             bg=self.colors["bg"], fg=self.colors["subtext"], font=("Segoe UI", 11, "italic"))
        intro_lbl.pack(anchor="w", padx=10, pady=(5, 15))

        for key, p in PROFILES.items():
            card = tk.Frame(self.profiles_scroll_frame, bg=self.colors["card_bg"], bd=1, relief="solid", highlightbackground=self.colors["card_border"])
            card.pack(fill="x", expand=True, padx=10, pady=8)

            top_row = tk.Frame(card, bg=self.colors["card_bg"])
            top_row.pack(fill="x", padx=15, pady=(12, 5))

            p_name = p["name"][self.lang]
            p_hint = p["gpu_hint"][self.lang]
            p_desc = p["desc"][self.lang]

            title = tk.Label(top_row, text=p_name, font=("Segoe UI", 12, "bold"),
                             bg=self.colors["card_bg"], fg=self.colors["fg"])
            title.pack(side="left")

            badge = tk.Label(top_row, text=f" {p['badge']} ", font=("Segoe UI", 8, "bold"),
                             bg=p["badge_color"], fg="#ffffff")
            badge.pack(side="left", padx=10)

            apply_btn = tk.Button(top_row, text=self.t("apply_profile"), bg=self.colors["accent"], fg="#11111b",
                                  font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=5,
                                  command=lambda p_data=p["data"], name=p_name: self.apply_profile_action(p_data, name))
            apply_btn.pack(side="right")

            gpu_hint = tk.Label(card, text=p_hint, font=("Segoe UI", 9, "bold"),
                                bg=self.colors["card_bg"], fg=self.colors["warning"], anchor="w")
            gpu_hint.pack(fill="x", padx=15, pady=(2, 4))

            desc = tk.Label(card, text=p_desc, font=("Segoe UI", 9),
                            bg=self.colors["card_bg"], fg=self.colors["subtext"], anchor="w", justify="left")
            desc.pack(fill="x", padx=15, pady=(0, 12))

    def build_custom_tab(self):
        canvas = tk.Canvas(self.tab_custom, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_custom, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors["bg"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        self.vars = {}

        # Section 1: Graphics
        self.gfx_frame = ttk.LabelFrame(scroll_frame, text=self.t("custom_gfx_header"), padding=15)
        self.gfx_frame.pack(fill="x", expand=True, padx=10, pady=8)

        self.lbl_tex_div = tk.Label(self.gfx_frame, text=self.t("tex_div_label"), font=("Segoe UI", 9, "bold"))
        self.lbl_tex_div.grid(row=0, column=0, sticky="w", pady=5)

        self.vars["dividetexturesize"] = tk.StringVar(value="0")
        self.tex_combo = ttk.Combobox(self.gfx_frame, textvariable=self.vars["dividetexturesize"], state="readonly", width=55)
        self.tex_combo.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        self.vars["dynamicshadows"] = tk.IntVar(value=0)
        self.cb_shadows = tk.Checkbutton(self.gfx_frame, text=self.t("shadows_cb"), 
                                         variable=self.vars["dynamicshadows"], bg=self.colors["card_bg"], fg=self.colors["fg"],
                                         selectcolor=self.colors["bg"], activebackground=self.colors["card_bg"], activeforeground=self.colors["fg"])
        self.cb_shadows.grid(row=1, column=0, columnspan=2, sticky="w", pady=4)

        self.vars["postprocessing"] = tk.IntVar(value=0)
        self.cb_post = tk.Checkbutton(self.gfx_frame, text=self.t("postproc_cb"), 
                                      variable=self.vars["postprocessing"], bg=self.colors["card_bg"], fg=self.colors["fg"],
                                      selectcolor=self.colors["bg"], activebackground=self.colors["card_bg"], activeforeground=self.colors["fg"])
        self.cb_post.grid(row=2, column=0, columnspan=2, sticky="w", pady=4)

        self.vars["useeffects"] = tk.IntVar(value=1)
        self.cb_shd = tk.Checkbutton(self.gfx_frame, text=self.t("shaders_cb"), 
                                     variable=self.vars["useeffects"], bg=self.colors["card_bg"], fg=self.colors["fg"],
                                     selectcolor=self.colors["bg"], activebackground=self.colors["card_bg"], activeforeground=self.colors["fg"])
        self.cb_shd.grid(row=3, column=0, columnspan=2, sticky="w", pady=4)

        self.vars["disableparticles"] = tk.IntVar(value=0)
        self.cb_part = tk.Checkbutton(self.gfx_frame, text=self.t("particles_cb"), 
                                      variable=self.vars["disableparticles"], bg=self.colors["card_bg"], fg=self.colors["fg"],
                                      selectcolor=self.colors["bg"], activebackground=self.colors["card_bg"], activeforeground=self.colors["fg"])
        self.cb_part.grid(row=4, column=0, columnspan=2, sticky="w", pady=4)

        # Section 2: Lightmapping
        self.light_frame = ttk.LabelFrame(scroll_frame, text=self.t("custom_light_header"), padding=15)
        self.light_frame.pack(fill="x", expand=True, padx=10, pady=8)

        self.lbl_ltex = tk.Label(self.light_frame, text=self.t("ltex_label"), font=("Segoe UI", 9, "bold"))
        self.lbl_ltex.grid(row=0, column=0, sticky="w", pady=5)

        self.vars["lightmaptexsize"] = tk.StringVar(value="512")
        self.ltex_combo = ttk.Combobox(self.light_frame, textvariable=self.vars["lightmaptexsize"], state="readonly", width=35)
        self.ltex_combo.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        self.lbl_lqual = tk.Label(self.light_frame, text=self.t("lqual_label"), font=("Segoe UI", 9, "bold"))
        self.lbl_lqual.grid(row=1, column=0, sticky="w", pady=5)

        self.vars["lightmapquality"] = tk.StringVar(value="20")
        lqual_entry = ttk.Entry(self.light_frame, textvariable=self.vars["lightmapquality"], width=10)
        lqual_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.lbl_lqual_hint = tk.Label(self.light_frame, text=self.t("lqual_hint"), font=("Segoe UI", 8), fg=self.colors["subtext"])
        self.lbl_lqual_hint.grid(row=1, column=2, sticky="w")

        self.vars["systemmemorycapoff"] = tk.IntVar(value=1)
        self.cb_ram = tk.Checkbutton(self.light_frame, text=self.t("ram_cap_cb"), 
                                     variable=self.vars["systemmemorycapoff"], bg=self.colors["card_bg"], fg=self.colors["fg"],
                                     selectcolor=self.colors["bg"], activebackground=self.colors["card_bg"], activeforeground=self.colors["fg"])
        self.cb_ram.grid(row=2, column=0, columnspan=3, sticky="w", pady=6)

        # Section 3: Engine & AI
        self.engine_frame = ttk.LabelFrame(scroll_frame, text=self.t("custom_engine_header"), padding=15)
        self.engine_frame.pack(fill="x", expand=True, padx=10, pady=8)

        self.lbl_ai = tk.Label(self.engine_frame, text=self.t("airadius_label"), font=("Segoe UI", 9, "bold"))
        self.lbl_ai.grid(row=0, column=0, sticky="w", pady=5)

        self.vars["airadius"] = tk.StringVar(value="20")
        ai_entry = ttk.Entry(self.engine_frame, textvariable=self.vars["airadius"], width=10)
        ai_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.lbl_ai_hint = tk.Label(self.engine_frame, text=self.t("airadius_hint"), font=("Segoe UI", 8), fg=self.colors["subtext"])
        self.lbl_ai_hint.grid(row=0, column=2, sticky="w")

        # Save Button
        self.save_custom_btn = tk.Button(scroll_frame, text=self.t("save_custom_btn"), bg=self.colors["success"], fg="#11111b",
                                         font=("Segoe UI", 11, "bold"), bd=0, padx=15, pady=8, command=self.save_manual_custom_action)
        self.save_custom_btn.pack(pady=15)

        self.update_custom_tab_translations()

    def update_custom_tab_translations(self):
        self.gfx_frame.config(text=self.t("custom_gfx_header"))
        self.lbl_tex_div.config(text=self.t("tex_div_label"))
        self.tex_combo.config(values=[
            self.t("tex_opt_0"), self.t("tex_opt_1"), self.t("tex_opt_2"), self.t("tex_opt_4")
        ])
        self.cb_shadows.config(text=self.t("shadows_cb"))
        self.cb_post.config(text=self.t("postproc_cb"))
        self.cb_shd.config(text=self.t("shaders_cb"))
        self.cb_part.config(text=self.t("particles_cb"))

        self.light_frame.config(text=self.t("custom_light_header"))
        self.lbl_ltex.config(text=self.t("ltex_label"))
        self.ltex_combo.config(values=[
            self.t("ltex_opt_256"), self.t("ltex_opt_512"), self.t("ltex_opt_1024"), self.t("ltex_opt_2048")
        ])
        self.lbl_lqual.config(text=self.t("lqual_label"))
        self.lbl_lqual_hint.config(text=self.t("lqual_hint"))
        self.cb_ram.config(text=self.t("ram_cap_cb"))

        self.engine_frame.config(text=self.t("custom_engine_header"))
        self.lbl_ai.config(text=self.t("airadius_label"))
        self.lbl_ai_hint.config(text=self.t("airadius_hint"))
        self.save_custom_btn.config(text=self.t("save_custom_btn"))

    def build_editor_tab(self):
        frame = tk.Frame(self.tab_editor, bg=self.colors["bg"])
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_bar = tk.Frame(frame, bg=self.colors["bg"])
        top_bar.pack(fill="x", pady=(0, 10))

        self.reload_btn = tk.Button(top_bar, text=self.t("reload_preview"), bg=self.colors["card_bg"], fg=self.colors["fg"],
                                    bd=1, relief="solid", padx=10, pady=5, command=self.load_editor_text)
        self.reload_btn.pack(side="left", padx=5)

        self.backup_btn = tk.Button(top_bar, text=self.t("create_backup_btn"), bg=self.colors["card_bg"], fg=self.colors["fg"],
                                    bd=1, relief="solid", padx=10, pady=5, command=self.create_manual_backup)
        self.backup_btn.pack(side="left", padx=5)

        self.editor_text = scrolledtext.ScrolledText(frame, bg="#11111b", fg="#a6e3a1", insertbackground="white",
                                                     font=("Consolas", 10), wrap="none")
        self.editor_text.pack(fill="both", expand=True)

        self.save_edit_btn = tk.Button(frame, text=self.t("save_editor_btn"), bg=self.colors["accent"], fg="#11111b",
                                       font=("Segoe UI", 10, "bold"), bd=0, padx=10, pady=6, command=self.save_raw_editor_text)
        self.save_edit_btn.pack(pady=(10, 0))

    def update_editor_tab_translations(self):
        self.reload_btn.config(text=self.t("reload_preview"))
        self.backup_btn.config(text=self.t("create_backup_btn"))
        self.save_edit_btn.config(text=self.t("save_editor_btn"))

    def browse_ini_file(self):
        path = filedialog.askopenfilename(title=self.t("select_file"), filetypes=[("INI files", "*.ini"), ("All files", "*.*")])
        if path:
            self.manager.filepath = path
            self.status_var.set(f"{self.t('status_file')} {path}")
            self.load_current_values()
            self.load_editor_text()

    def load_current_values(self):
        if not self.manager.exists():
            return
        data = self.manager.get_all_settings()
        gamerun = data.get("GAMERUN", {})
        gamemake = data.get("GAMEMAKE", {})

        div_val = gamerun.get("dividetexturesize", "0")
        opts = [self.t("tex_opt_0"), self.t("tex_opt_1"), self.t("tex_opt_2"), self.t("tex_opt_4")]
        for opt in opts:
            if opt.startswith(div_val):
                self.vars["dividetexturesize"].set(opt)

        self.vars["dynamicshadows"].set(int(gamerun.get("dynamicshadows", "0")))
        self.vars["postprocessing"].set(int(gamerun.get("postprocessing", "0")))
        self.vars["useeffects"].set(int(gamerun.get("useeffects", "1")))
        self.vars["disableparticles"].set(int(gamerun.get("disableparticles", "0")))

        lsize = gamemake.get("lightmaptexsize", "512")
        lopts = [self.t("ltex_opt_256"), self.t("ltex_opt_512"), self.t("ltex_opt_1024"), self.t("ltex_opt_2048")]
        for lopt in lopts:
            if lopt.startswith(lsize):
                self.vars["lightmaptexsize"].set(lopt)

        self.vars["lightmapquality"].set(gamemake.get("lightmapquality", "20"))
        self.vars["systemmemorycapoff"].set(int(gamemake.get("systemmemorycapoff", "1")))
        self.vars["airadius"].set(gamerun.get("airadius", "20"))

        self.load_editor_text()

    def load_editor_text(self):
        lines = self.manager.read_lines()
        self.editor_text.delete("1.0", tk.END)
        self.editor_text.insert(tk.END, "".join(lines))

    def create_manual_backup(self):
        bpath = self.manager.create_backup()
        if bpath:
            messagebox.showinfo(self.t("backup_success"), f"{self.t('backup_success_msg')}{os.path.basename(bpath)}")
        else:
            messagebox.showerror(self.t("error"), self.t("backup_error"))

    def apply_profile_action(self, profile_data: dict, profile_name: str):
        if not self.manager.exists():
            messagebox.showerror(self.t("error"), f"{self.t('file_not_found')} ({self.manager.filepath})")
            return

        if messagebox.askyesno(self.t("confirm_profile_title"), f"{self.t('confirm_profile_msg')}'{profile_name}'?"):
            if self.manager.apply_dict_updates(profile_data, auto_backup=True):
                messagebox.showinfo(self.t("success"), self.t("profile_applied"))
                self.load_current_values()
            else:
                messagebox.showerror(self.t("error"), self.t("write_error"))

    def save_manual_custom_action(self):
        if not self.manager.exists():
            messagebox.showerror(self.t("error"), f"{self.t('file_not_found')} ({self.manager.filepath})")
            return

        tex_val = self.vars["dividetexturesize"].get().split(" ")[0]
        lsize_val = self.vars["lightmaptexsize"].get().split(" ")[0]

        updates = {
            "GAMERUN": {
                "dividetexturesize": tex_val,
                "dynamicshadows": str(self.vars["dynamicshadows"].get()),
                "postprocessing": str(self.vars["postprocessing"].get()),
                "useeffects": str(self.vars["useeffects"].get()),
                "disableparticles": str(self.vars["disableparticles"].get()),
                "airadius": str(self.vars["airadius"].get().strip())
            },
            "GAMEMAKE": {
                "lightmaptexsize": lsize_val,
                "lightmapquality": str(self.vars["lightmapquality"].get().strip()),
                "systemmemorycapoff": str(self.vars["systemmemorycapoff"].get())
            }
        }

        if self.manager.apply_dict_updates(updates, auto_backup=True):
            messagebox.showinfo(self.t("success"), self.t("save_success"))
            self.load_current_values()
        else:
            messagebox.showerror(self.t("error"), self.t("write_error"))

    def save_raw_editor_text(self):
        content = self.editor_text.get("1.0", tk.END)
        self.manager.create_backup()
        lines = content.splitlines(keepends=True)
        if self.manager.write_lines(lines):
            messagebox.showinfo(self.t("success"), self.t("save_success"))
            self.load_current_values()
        else:
            messagebox.showerror(self.t("error"), self.t("write_error"))

def run_cli_mode(manager: SetupIniManager):
    """Console Interface (CLI) with Language Switcher."""
    lang = "en"
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        t = TRANSLATIONS[lang]
        print("================================================================")
        print(t["cli_title"])
        print("================================================================")
        print(f" {t['cli_current']} {manager.filepath}\n")

        print(f"{t['cli_available']}")
        for key, profile in PROFILES.items():
            print(f" [{key}] {profile['name'][lang]}")
            print(f"     💡 {profile['gpu_hint'][lang]}")
            print(f"     📝 {profile['desc'][lang]}\n")

        print(" --------------------------------------------------------------")
        print(t["cli_option_m"])
        print(t["cli_option_b"])
        print(t["cli_option_l"])
        print(t["cli_option_0"])
        print("================================================================")

        choice = input(f"\n{t['cli_prompt']}").strip().upper()

        if choice in PROFILES:
            p = PROFILES[choice]
            print(f"\nApplying profile: {p['name'][lang]}...")
            if manager.apply_dict_updates(p['data'], auto_backup=True):
                print("[+] Success!")
            else:
                print("[!] Error applying profile.")
            input("\nPress Enter to continue...")

        elif choice == "M":
            lines = manager.read_lines()
            print("\n--- Manual Tweaks ---")
            val = input("Texture Divider [0=Full, 1=50%, 2=25%/Intel HD, 4=Retro]: ").strip()
            if val in ["0", "1", "2", "4"]:
                lines = manager.update_key_in_lines(lines, "GAMERUN", "dividetexturesize", val)

            val = input("Dynamic Shadows [0=Off, 1=On]: ").strip()
            if val in ["0", "1"]:
                lines = manager.update_key_in_lines(lines, "GAMERUN", "dynamicshadows", val)

            val = input("Post Processing [0=Off, 1=On]: ").strip()
            if val in ["0", "1"]:
                lines = manager.update_key_in_lines(lines, "GAMERUN", "postprocessing", val)

            manager.create_backup()
            manager.write_lines(lines)
            print("\n[+] Settings saved!")
            input("\nPress Enter to continue...")

        elif choice == "B":
            bpath = manager.create_backup()
            if bpath:
                print(f"\n[+] Backup created: {os.path.basename(bpath)}")
            else:
                print("\n[!] Failed to create backup.")
            input("\nPress Enter to continue...")

        elif choice == "L":
            lang = "sk" if lang == "en" else "en"

        elif choice == "0":
            break

def main():
    manager = SetupIniManager(INI_FILE_NAME)

    if not manager.exists():
        print(f"[!] Warning: '{INI_FILE_NAME}' not found in current folder.")

    if GUI_AVAILABLE and "--cli" not in sys.argv:
        root = tk.Tk()
        app = ConfiguratorGUI(root, manager)
        root.mainloop()
    else:
        run_cli_mode(manager)

if __name__ == "__main__":
    main()