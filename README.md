# MyClock — relógio de desktop personalizável

Um relógio para Windows pensado para ficar presente sem chamar atenção demais.  
A ideia é simples: transformar momentos de pausa do computador em algo mais limpo, agradável e visualmente calmo — com uma hora fácil de ler, uma data elegante e uma pequena frase que muda diariamente.

O projeto foi desenvolvido com foco em três coisas:

- visual minimalista;
- personalização rápida;
- código organizado o suficiente para continuar evoluindo sem virar caos.

---

## A ideia por trás do projeto

Muitas vezes eu queria deixar o computador “parado” sem abrir navegador, player ou alguma interface cheia de elementos. Só um relógio grande, bonito e confortável de olhar à distância.

O MyClock começou exatamente assim: primeiro como uma janela simples mostrando a hora, depois ganhando temas, ajustes de fonte, persistência de configurações e, mais tarde, a geração automática de citações diárias via API.

Hoje ele funciona quase como uma pequena “tela ambiente” para o desktop — discreta, configurável e leve.

---

## O que já está funcionando

### Experiência geral

A interface principal mantém tudo centralizado e fácil de ler:

- **hora** em destaque;
- **data** em formato longo;
- **uma citação curta** exibida logo abaixo.

Os tamanhos seguem uma hierarquia proporcional para manter a composição equilibrada visualmente.

O painel de configurações também foi pensado para não poluir a tela: ele aparece apenas quando o cursor se aproxima da borda esquerda da janela e desaparece automaticamente quando não está sendo usado.  
A intenção era deixar o relógio “respirar”, sem parecer um aplicativo cheio de menus o tempo inteiro.

---

### Relógio e atualização de tempo

O sistema de tempo roda através de um `ClockEngine`, usando `QTimer` em modo preciso para atualizar o relógio a cada segundo.

Atualmente ele suporta:

- formato **24h ou 12h**;
- opção de **mostrar ou ocultar segundos**;
- atualização contínua da data.

A data utiliza listas próprias de dias e meses para manter consistência visual independentemente do locale do Windows.

---

### Aparência e personalização

Os temas são definidos em JSON (`assets/themes/presets.json`) e separados entre modos claros e escuros.

Cada preset possui:

- identificador interno;
- nome exibido no tooltip;
- cor de fundo;
- cor principal do texto.

Além dos presets prontos, existe também o modo **custom**, onde o usuário pode escolher livremente a cor de fundo usando o seletor do Qt.

A parte tipográfica também é totalmente ajustável: fonte e tamanho podem ser alterados diretamente pelo painel lateral.  
A seleção inclui fontes comuns no Windows, tanto monoespaçadas quanto sans-serif, buscando manter boa legibilidade em diferentes tamanhos de janela.

Todas as preferências são salvas automaticamente em:

```txt
neoclock/data/settings.json
```

Assim, ao abrir o aplicativo novamente, tudo volta exatamente como estava.

---

### Citação diária

O `QuoteEngine` integra a API da **Groq** para gerar uma pequena citação reflexiva por dia.

As frases podem vir em português ou inglês e ficam armazenadas localmente para evitar chamadas repetidas durante o mesmo dia. Isso mantém a experiência consistente e reduz uso desnecessário da API.

Caso a requisição falhe, o aplicativo utiliza uma mensagem de fallback amigável em vez de interromper a interface.

Para ativar essa funcionalidade, basta definir a variável:

```env
GROQ_API_KEY=sua_chave_aqui
```

Ela pode ser carregada via `.env` usando `python-dotenv`.

---

## Estrutura do projeto

| Camada | Responsabilidade |
|--------|--------|
| `main.py` | Inicializa o `QApplication` e cria a janela principal. |
| `core/settings_manager.py` | Gerencia presets, defaults e persistência do `settings.json`. |
| `core/clock_engine.py` | Atualização e formatação de hora/data. |
| `core/quote_engine.py` | Geração e cache da citação diária via Groq. |
| `ui/main_window.py` | Organização da janela, painel lateral, eventos de mouse e integração geral. |
| `ui/clock_widget.py` | Renderização dos textos e aplicação dinâmica de estilos. |
| `ui/settings_panel.py` | Controles de tema, fonte, tamanho e animações do painel. |

De forma geral, o fluxo do app funciona assim:

```txt
ClockEngine → atualiza horário
SettingsPanel → altera configurações
MainWindow → reaplica estilos e sincroniza interface
```

---

## Como executar

### Requisitos

- Python 3
- PySide6
- dependências utilizadas pelo projeto

Dentro da pasta `neoclock`:

```bash
python -m venv .venv
.venv\Scripts\activate

pip install PySide6 groq python-dotenv

python main.py
```

Depois, crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_aqui
```

Sem uma chave válida, o sistema de citações pode usar o fallback local dependendo da resposta da API.

---

## Estrutura de pastas

```txt
neoclock/
  main.py
  core/           # lógica principal e persistência
  ui/             # interface e componentes visuais
  assets/themes/  # presets.json
  data/           # settings.json gerado em runtime
```

---

## Personalização rápida

### Adicionar novos temas

Edite:

```txt
neoclock/assets/themes/presets.json
```

E adicione novos objetos em `dark` ou `light` contendo:

```json
{
  "id": "novo_tema",
  "label": "Novo Tema",
  "background_color": "#000000",
  "text_color": "#ffffff"
}
```

---

### Adicionar novas fontes

Basta incluir a família tipográfica na lista `FONTS` em:

```txt
neoclock/ui/settings_panel.py
```

O nome precisa corresponder a uma fonte instalada no sistema.

---

## Licença

O projeto segue os termos definidos no arquivo `LICENSE`.

Integrações externas, como a API da Groq, continuam sujeitas aos limites e políticas dos respectivos serviços.

---

*README atualizado de acordo com o estado atual do projeto. Conforme novas funcionalidades forem adicionadas, essa documentação pode evoluir junto com a aplicação.*