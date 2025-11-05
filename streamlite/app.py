import streamlit as st
from datetime import datetime

# --- State (équivalent de data() dans Vue) ---
if "active_view" not in st.session_state:
    st.session_state.active_view = "chat"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"type": "answer", "text": "Bonjour — tu peux poser une question à propos des documents importés.", "time": datetime.now().strftime("%H:%M")}
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# --- Sidebar (Navigation) ---
st.sidebar.title("Mini RAG")

if st.sidebar.button("📄 Importer", key="import_btn"):
    st.session_state.active_view = "upload"

if st.sidebar.button("💬 Nouveau Chat", key="newchat_btn"):
    st.session_state.active_view = "chat"
    st.session_state.messages = [
        {"type": "answer", "text": "Nouveau chat démarré.", "time": datetime.now().strftime("%H:%M")}
    ]

if st.sidebar.button("🕘 Historique", key="history_btn"):
    st.session_state.active_view = "history"

if st.sidebar.button("📚 Documentation", key="docs_btn"):
    st.session_state.active_view = "docs"

st.sidebar.markdown("---")
st.sidebar.subheader("Historique récent :")
for idx, h in enumerate(st.session_state.history[:6]):
    st.sidebar.write(f"• {h['question'][:30]}...")

# --- Main Title ---
st.title("Système RAG pour recherche documentaire")

# ========== 1) UPLOAD VIEW ==========
if st.session_state.active_view == "upload":
    st.subheader("Importer un document")
    uploaded = st.file_uploader("Choisir un fichier (PDF / DOCX)", type=["pdf", "docx"], key="file_uploader")

    if uploaded:
        st.session_state.uploaded_file = uploaded
        st.success(f"Fichier sélectionné : **{uploaded.name}**")

        if st.button("➡️ Envoyer et indexer", key="send_index_btn"):
            # À remplacer plus tard par l’indexation réelle FAISS / Chroma
            st.session_state.history.insert(
                0,
                {"question": f"Document importé: {uploaded.name}", "time": datetime.now().strftime("%d/%m %H:%M")}
            )
            st.success("Indexation terminée ✅")
            st.rerun()  # relance le script pour mettre à jour l'UI

# ========== 2) CHAT VIEW ==========
elif st.session_state.active_view == "chat":
    for msg in st.session_state.messages:
        speaker = "Vous" if msg["type"] == "question" else "RAG"
        st.markdown(f"**{speaker}** ({msg['time']}) : {msg['text']}")  # pas de key ici

    user_input = st.text_input("Posez votre question...", key="user_input")

    if st.button("Envoyer", key="send_btn") and user_input.strip() != "":
        st.session_state.messages.append(
            {"type": "question", "text": user_input, "time": datetime.now().strftime("%H:%M")}
        )
        st.session_state.history.insert(
            0,
            {"question": user_input, "time": datetime.now().strftime("%d/%m %H:%M")}
        )

        # Réponse simulée
        answer = f"Voici une réponse à : **{user_input}** (réponse simulée)"
        st.session_state.messages.append(
            {"type": "answer", "text": answer, "time": datetime.now().strftime("%H:%M")}
        )
        st.rerun()  # relance le script pour afficher le nouveau message

# ========== 3) HISTORY VIEW ==========
elif st.session_state.active_view == "history":
    st.subheader("Historique des questions")
    if len(st.session_state.history) == 0:
        st.info("Aucune question pour le moment.")
    else:
        for h in st.session_state.history:
            st.write(f"• **{h['question']}** — _{h['time']}_")  # pas de key ici

# ========== 4) DOCS VIEW ==========
elif st.session_state.active_view == "docs":
    st.subheader("Documentation / Aide")
    st.write("""
1. Aller dans **Importer** pour ajouter un PDF ou DOCX.
2. Cliquez **Envoyer et indexer** pour l’ajouter à la base vecteur.
3. Allez dans **Chat** pour poser une question.
4. Le système affichera la réponse + les sources.
""")
