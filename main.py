import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Conectar ao banco de dados de alunos
conn_alunos = sqlite3.connect('alunos.db')
cursor_alunos = conn_alunos.cursor()

# Criar tabela de alunos se não existir
cursor_alunos.execute('''
CREATE TABLE IF NOT EXISTS Alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    cidade_id INTEGER,
    FOREIGN KEY (cidade_id) REFERENCES Cidades(id)
)
''')
conn_alunos.commit()

# Conectar ao banco de dados de cidades
conn_cidades = sqlite3.connect('cidades.db')
cursor_cidades = conn_cidades.cursor()

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro de Alunos")

        self.nome_var = tk.StringVar()
        self.idade_var = tk.IntVar()
        self.cidade_var = tk.StringVar()

        self.create_widgets()
        self.carregar_cidades()
        self.carregar_alunos()

    def create_widgets(self):
        # Campos de entrada
        tk.Label(self.master, text="Nome").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.nome_var).grid(row=0, column=1)

        tk.Label(self.master, text="Idade").grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.idade_var).grid(row=1, column=1)

        tk.Label(self.master, text="Cidade").grid(row=2, column=0)
        self.cidade_combobox = ttk.Combobox(self.master, textvariable=self.cidade_var)
        self.cidade_combobox.grid(row=2, column=1)

        # Botões
        tk.Button(self.master, text="Incluir", command=self.incluir_aluno).grid(row=3, column=0)
        tk.Button(self.master, text="Alterar", command=self.alterar_aluno).grid(row=3, column=1)
        tk.Button(self.master, text="Excluir", command=self.excluir_aluno).grid(row=3, column=2)

        # TreeView
        self.tree = ttk.Treeview(self.master, columns=('Nome', 'Idade', 'Cidade'), show='headings')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Idade', text='Idade')
        self.tree.heading('Cidade', text='Cidade')
        self.tree.grid(row=4, column=0, columnspan=3)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def carregar_cidades(self):
        cursor_cidades.execute("SELECT * FROM Cidades")
        cidades = cursor_cidades.fetchall()
        self.cidade_combobox['values'] = [f"{cidade[1]} (ID: {cidade[0]})" for cidade in cidades]

    def carregar_alunos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor_alunos.execute("SELECT a.id, a.nome, a.idade, c.nome FROM Alunos a LEFT JOIN Cidades c ON a.cidade_id = c.id")
        for row in cursor_alunos.fetchall():
            self.tree.insert('', 'end', values=(row[1], row[2], row[3]), tags=(row[0],))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            self.nome_var.set(item['values'][0])
            self.idade_var.set(item['values'][1])
            self.cidade_combobox.set(item['values'][2])

    def incluir_aluno(self):
        nome = self.nome_var.get()
        idade = self.idade_var.get()
        cidade_id = self.cidade_combobox.get().split(" (ID: ")[-1][:-1]
        if nome and idade and cidade_id:
            cursor_alunos.execute("INSERT INTO Alunos (nome, idade, cidade_id) VALUES (?, ?, ?)", (nome, idade, cidade_id))
            conn_alunos.commit()
            self.carregar_alunos()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos")

    def alterar_aluno(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_aluno = self.tree.item(selected_item, 'tags')[0]
            nome = self.nome_var.get()
            idade = self.idade_var.get()
            cidade_id = self.cidade_combobox.get().split(" (ID: ")[-1][:-1]
            cursor_alunos.execute("UPDATE Alunos SET nome=?, idade=?, cidade_id=? WHERE id=?", (nome, idade, cidade_id, id_aluno))
            conn_alunos.commit()
            self.carregar_alunos()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Selecione um aluno para alterar")

    def excluir_aluno(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_aluno = self.tree.item(selected_item, 'tags')[0]
            cursor_alunos.execute("DELETE FROM Alunos WHERE id=?", (id_aluno,))
            conn_alunos.commit()
            self.carregar_alunos()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Selecione um aluno para excluir")

    def limpar_campos(self):
        self.nome_var.set("")
        self.idade_var.set(0)
        self.cidade_combobox.set("")

# Inicializar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

    # Fechar as conexões ao sair
    conn_alunos.close()
    conn_cidades.close()
