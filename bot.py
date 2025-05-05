import asyncio
import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.ext import MessageHandler, filters

# Lista para armazenar quem está no modo atendimento
usuarios_atendimento = set()

# Carrega o arquivo de respostas
with open("respostas.json", "r", encoding="utf-8") as f:
    respostas = json.load(f)

# Token do ChatBot
TOKEN = "7865550052:AAEnacYWJczbwwyGrVYpKZvbzCpRi_HZbuw"

# Função para o /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔊 Raaawr! Eu sou o Panthera da FURIA 🐆. Pronto pra conversar comigo?\nEscolha uma opção:",
        reply_markup=main_menu()
    )

# Função para construir o menu principal
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📚 História", callback_data="historia")],
        [InlineKeyboardButton("🎯 Time de CS", callback_data="cs")],
        [InlineKeyboardButton("🛒 Loja Oficial", callback_data="loja")],
        [InlineKeyboardButton("💡 Institucional", callback_data="institucional")],
        [InlineKeyboardButton("🎲 Surpresa!", callback_data="surpresa")],
        [InlineKeyboardButton("📞 Fale Conosco!", callback_data="fale_conosco")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Função para submenu de Fale Conosco
def fale_conosco_menu():
    keyboard = [
        [InlineKeyboardButton("💬 Dúvidas/Sugestões", callback_data="duvidas")],
        [InlineKeyboardButton("🧑‍💼 Trabalhe Conosco", callback_data="trabalhe")],
        [InlineKeyboardButton("📢 Fale com um Atendente!", callback_data="outra_opcao")],
        [InlineKeyboardButton("⬅️ Voltar ao Menu Principal", callback_data="menu_principal")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Retorno das mensagens recebidas pelo ChatBot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if user.id not in usuarios_atendimento:
        await update.message.reply_text(
            "⚠️ Para falar com um atendente, clique primeiro em 📞 Fale Conosco > 📢 Fale com um Atendente!")
        return

    admin_chat_id = 662654989

    # Formato da mensagem enviada para o admin
    message_to_admin = f"📨 Nova mensagem de @{user.username} (ID: {user.id}):\n{text}"

    await context.bot.send_message(chat_id=admin_chat_id, text=message_to_admin)

    # Confirmação para o usuário
    await update.message.reply_text("✅ Obrigado pela sua mensagem! Um atendente vai te responder em breve. 🐆")


# Função para lidar com cliques nos botões
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "historia":
        await query.message.reply_photo(
            photo=open("historia.jpg", "rb"),
            caption=respostas["historia"]
        )
    elif choice == "cs":
        await query.message.reply_text(respostas["cs"])
    elif choice == "loja":
        await query.message.reply_text(respostas["loja"])
    elif choice == "institucional":
        await query.message.reply_text(respostas["institucional"])
    elif choice == "surpresa":
        curiosidade = random.choice(respostas["curiosidades"])
        await query.message.reply_voice(
            voice=open("surpresa.ogg", "rb"),
            caption="🔊 Aumenta o som aí!"
        )
        await query.message.reply_text(curiosidade)
    elif choice == "fale_conosco":
        await query.message.reply_text(
            "📞 Bem-vindo ao Fale Conosco! Escolha uma opção:",
            reply_markup=fale_conosco_menu()
        )
        return
    elif choice == "duvidas":
        await query.message.reply_text(respostas["fale_conosco_duvidas"])
    elif choice == "trabalhe":
        await query.message.reply_text(respostas["fale_conosco_trabalhe"])
    elif choice == "outra_opcao":
        user_id = query.from_user.id
        usuarios_atendimento.add(user_id)
        await query.message.reply_text(respostas["fale_conosco_outra_opcao"])
        return
    elif choice == "menu_principal":
        await query.message.reply_text(
            "⬅️ Voltando ao menu principal...",
            reply_markup=main_menu()
        )
        return

    # Ao final de qualquer resposta (exceto quando já voltou ao menu), mostrar menu novamente
    await asyncio.sleep(3)
    await query.message.reply_text(
        "⬅️ Quer voltar ao menu principal?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Voltar ao Menu Principal", callback_data="menu_principal")]
        ])
    )

# Função principal
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot está rodando... 🐾")
    app.run_polling()

# Rodando o bot
if __name__ == "__main__":
    main()
