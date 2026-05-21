import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyttsx3
import threading

try:
    lang_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    lang_names = sorted(lang_dict.keys())
except:
    lang_names = ["english", "french", "spanish", "german", "italian"]
    lang_dict = {nom: nom[:2] for nom in lang_names}

lang_names_with_auto = ["Détection auto"] + lang_names
lang_dict["Détection auto"] = "auto"

engine = pyttsx3.init()

def traduction_async():
    threading.Thread(target=traduire, daemon=True).start()

def traduire():
    texte = text_source.get("1.0", tk.END).strip()
    if not texte:
        messagebox.showwarning("Attention", "Entrez du texte à traduire")
        return

    src_nom = combo_source.get()
    tgt_nom = combo_cible.get()
    src_code = lang_dict[src_nom]
    tgt_code = lang_dict[tgt_nom]

    if src_code == "auto":
        src_code = None

    try:
        resultat = GoogleTranslator(source=src_code, target=tgt_code).translate(texte)
        text_target.config(state=tk.NORMAL)
        text_target.delete("1.0", tk.END)
        text_target.insert(tk.END, resultat)
        text_target.config(state=tk.DISABLED)

        if src_nom == "Détection auto":
            detected = GoogleTranslator().detect(texte)
            if detected and detected[0] in lang_dict.values():
                for nom, code in lang_dict.items():
                    if code == detected[0] and nom != "Détection auto":
                        combo_source.set(nom)
                        break
    except Exception as e:
        messagebox.showerror("Erreur", f"Traduction échouée : {e}")

def echanger_langues():
    src = combo_source.get()
    tgt = combo_cible.get()
    if src == "Détection auto":
        messagebox.showwarning("Impossible", "Échange non autorisé avec détection auto")
        return
    combo_source.set(tgt)
    combo_cible.set(src)
    if text_source.get("1.0", tk.END).strip():
        traduire()

def copier_vers_presse_papiers():
    contenu = text_target.get("1.0", tk.END).strip()
    if contenu:
        fenetre.clipboard_clear()
        fenetre.clipboard_append(contenu)
        messagebox.showinfo("Copié", "Traduction copiée")
    else:
        messagebox.showwarning("Rien", "Aucune traduction")

def lire_texte(texte):
    if texte:
        engine.say(texte)
        engine.runAndWait()

def lire_source():
    lire_texte(text_source.get("1.0", tk.END).strip())

def lire_cible():
    lire_texte(text_target.get("1.0", tk.END).strip())

def effacer():
    text_source.delete("1.0", tk.END)
    text_target.config(state=tk.NORMAL)
    text_target.delete("1.0", tk.END)
    text_target.config(state=tk.DISABLED)

fenetre = tk.Tk()
fenetre.title("Traducteur Professionnel - CodeAlpha")
fenetre.geometry("950x600")
fenetre.configure(bg="#f5f5f5")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f5f5f5")
style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 10))

main_frame = ttk.Frame(fenetre, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

lang_frame = ttk.Frame(main_frame)
lang_frame.pack(fill=tk.X, pady=(0, 15))

ttk.Label(lang_frame, text="Source :").grid(row=0, column=0, padx=5, sticky="w")
combo_source = ttk.Combobox(lang_frame, values=lang_names_with_auto, state="readonly", width=20)
combo_source.grid(row=0, column=1, padx=5)
combo_source.set("Détection auto")

btn_swap = tk.Button(lang_frame, text="⇄", command=echanger_langues,
                     bg="#6c757d", fg="white", font=("Segoe UI", 10, "bold"),
                     relief=tk.FLAT, padx=10, pady=2, cursor="hand2")
btn_swap.grid(row=0, column=2, padx=15)

ttk.Label(lang_frame, text="Cible :").grid(row=0, column=3, padx=5, sticky="w")
combo_cible = ttk.Combobox(lang_frame, values=lang_names, state="readonly", width=20)
combo_cible.grid(row=0, column=4, padx=5)
combo_cible.set("french")

lang_frame.columnconfigure(5, weight=1)

text_frame = ttk.Frame(main_frame)
text_frame.pack(fill=tk.BOTH, expand=True)

text_frame.columnconfigure(0, weight=1)
text_frame.columnconfigure(1, weight=1)

left_frame = ttk.Frame(text_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

ttk.Label(left_frame, text="Texte original :", font=("Segoe UI", 10, "bold")).pack(anchor="w")
text_source = tk.Text(left_frame, height=12, font=("Segoe UI", 11), wrap=tk.WORD,
                      relief=tk.FLAT, borderwidth=1, highlightthickness=1, highlightbackground="#ccc")
text_source.pack(fill=tk.BOTH, expand=True, pady=5)

source_btn_frame = ttk.Frame(left_frame)
source_btn_frame.pack(fill=tk.X, pady=5)
btn_lire_src = tk.Button(source_btn_frame, text="🔊 Lire le texte source", command=lire_source,
                         bg="#17a2b8", fg="white", relief=tk.FLAT, padx=5, cursor="hand2")
btn_lire_src.pack(side=tk.LEFT, padx=2)
btn_effacer = tk.Button(source_btn_frame, text="🗑 Effacer", command=effacer,
                        bg="#dc3545", fg="white", relief=tk.FLAT, padx=5, cursor="hand2")
btn_effacer.pack(side=tk.LEFT, padx=2)

right_frame = ttk.Frame(text_frame)
right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

ttk.Label(right_frame, text="Traduction :", font=("Segoe UI", 10, "bold")).pack(anchor="w")
text_target = tk.Text(right_frame, height=12, font=("Segoe UI", 11), wrap=tk.WORD,
                      relief=tk.FLAT, borderwidth=1, highlightthickness=1, highlightbackground="#ccc",
                      state=tk.DISABLED, bg="#fafafa")
text_target.pack(fill=tk.BOTH, expand=True, pady=5)

target_btn_frame = ttk.Frame(right_frame)
target_btn_frame.pack(fill=tk.X, pady=5)
btn_copier = tk.Button(target_btn_frame, text="📋 Copier", command=copier_vers_presse_papiers,
                       bg="#28a745", fg="white", relief=tk.FLAT, padx=5, cursor="hand2")
btn_copier.pack(side=tk.LEFT, padx=2)
btn_lire_tgt = tk.Button(target_btn_frame, text="🔊 Lire la traduction", command=lire_cible,
                         bg="#17a2b8", fg="white", relief=tk.FLAT, padx=5, cursor="hand2")
btn_lire_tgt.pack(side=tk.LEFT, padx=2)

btn_traduire = tk.Button(main_frame, text="TRADUIRE", command=traduction_async,
                         bg="#007bff", fg="white", font=("Segoe UI", 12, "bold"),
                         padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
btn_traduire.pack(pady=15)

status = ttk.Label(main_frame, text="Prêt", relief=tk.SUNKEN, anchor=tk.W)
status.pack(fill=tk.X, side=tk.BOTTOM, pady=(10,0))

fenetre.mainloop()