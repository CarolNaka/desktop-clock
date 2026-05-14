# MyClock — relógio de desktop personalizável

Um relógio para Windows pensado para ficar presente sem chamar atenção demais.
A ideia é simples: transformar momentos de pausa do computador em algo mais limpo, agradável e visualmente calmo — com uma hora fácil de ler, uma data elegante, uma pequena frase diária e agora também uma experiência sonora ambiente.

O projeto foi desenvolvido com foco em quatro pilares:

* visual minimalista;
* personalização rápida;
* ambientação visual e sonora;
* código organizado o suficiente para continuar evoluindo sem virar caos.

---

# A ideia por trás do projeto

Muitas vezes eu queria deixar o computador “parado” sem abrir navegador, player ou alguma interface cheia de elementos. Só um relógio grande, bonito e confortável de olhar à distância.

O MyClock começou exatamente assim: primeiro como uma janela simples mostrando a hora, depois ganhando temas, ajustes de fonte, persistência de configurações e, mais tarde, geração automática de citações diárias via API.

Com o tempo, o projeto evoluiu para uma pequena experiência ambiente para desktop: um relógio discreto, configurável, com temas suaves, efeitos visuais animados e sons ambientes opcionais.

Hoje ele funciona quase como uma “tela de descanso minimalista” para o computador.

---

# O que já está funcionando

## Experiência geral

A interface principal mantém tudo centralizado e fácil de ler:

* **hora** em destaque;
* **data** em formato longo;
* **uma citação curta** exibida logo abaixo.

Os tamanhos seguem uma hierarquia proporcional para manter a composição equilibrada visualmente.

O painel de configurações foi pensado para não poluir a tela: ele aparece apenas quando o cursor se aproxima da borda esquerda da janela e desaparece automaticamente quando não está sendo usado.

Além disso:

* o menu agora possui scroll interno automático;
* funciona melhor em telas menores;
* evita cortes de interface;
* mantém todas as configurações acessíveis mesmo com muitos recursos ativos.

---

# Relógio e atualização de tempo

O sistema de tempo roda através de um `ClockEngine`, utilizando `QTimer` em modo preciso para atualizar o relógio a cada segundo.

Atualmente ele suporta:

* formato **24h ou 12h**;
* opção de **mostrar ou ocultar segundos**;
* atualização contínua da data;
* notificação sonora em hora cheia.

A data utiliza listas próprias de dias e meses para manter consistência visual independentemente do locale do Windows.

---

# Sistema de áudio ambiente

O projeto agora possui um sistema de áudio ambiente integrado.

## Música de fundo

Atualmente existe suporte para:

* lo-fi ambiente em loop;
* controle independente de reprodução;
* controle de volume integrado diretamente no menu;
* persistência automática das preferências;
* fade in/fade out suaves.

A reprodução respeita políticas de autoplay do sistema e só inicia após interação do usuário.

---

## Sons ambientes

Além da música de fundo, o projeto também suporta efeitos sonoros ambientes independentes.

Atualmente:

* chuva leve (`rain-01`);
* chuva intensa (`rain-02`).

Os sons ambientes:

* funcionam em loop;
* possuem volume independente;
* podem ser utilizados junto do lo-fi;
* permitem apenas um ambiente ativo por vez.

---

## Notificação horária

O sistema também suporta um toque suave em cada hora cheia utilizando:

* `ring-01.mp3`

O recurso pode ser ativado ou desativado nas configurações e possui volume independente.

---

# Aparência e personalização

Os temas são definidos em JSON (`assets/themes/presets.json`) e separados entre modos claros e escuros.

Cada preset possui:

* identificador interno;
* nome exibido no tooltip;
* cor de fundo;
* cor principal do texto.

Além dos presets prontos, existe também o modo **custom**, onde o usuário pode escolher livremente a cor de fundo usando o seletor do Qt.

---

## Background animado

Os temas agora suportam uma camada visual inspirada em ambientação oceânica minimalista.

O efeito inclui:

* textura animada;
* ondas suaves;
* movimentação contínua;
* integração com os temas claros e escuros.

A intenção é criar uma sensação mais relaxante sem transformar o relógio em uma interface visualmente pesada.

---

## Tipografia

A parte tipográfica também é totalmente ajustável:

* fonte;
* tamanho;
* proporção visual.

Tudo pode ser alterado diretamente pelo painel lateral.

A seleção inclui fontes comuns no Windows, tanto monoespaçadas quanto sans-serif, buscando manter boa legibilidade em diferentes tamanhos de janela.

---

# Persistência de configurações

Todas as preferências são salvas automaticamente em:

```txt
neoclock/data/settings.json
```

Incluindo:

* tema selecionado;
* fonte;
* tamanho;
* música ambiente;
* som de chuva;
* volumes;
* notificações;
* preferências visuais.

Ao abrir o aplicativo novamente, tudo retorna exatamente ao estado anterior.

---

# Citação diária

O `QuoteEngine` integra a API da Groq para gerar uma pequena citação reflexiva por dia.

As frases podem vir em português ou inglês e ficam armazenadas localmente para evitar chamadas repetidas durante o mesmo dia. Isso mantém a experiência consistente e reduz uso desnecessário da API.

Caso a requisição falhe, o aplicativo utiliza uma mensagem de fallback amigável em vez de interromper a interface.

Para ativar essa funcionalidade:

```env
GROQ_API_KEY=sua_chave_aqui
```

A variável pode ser carregada via `.env` utilizando `python-dotenv`.

---

# Estrutura do projeto

| Camada                     | Responsabilidade                                                 |
| -------------------------- | ---------------------------------------------------------------- |
| `main.py`                  | Inicializa o `QApplication` e cria a janela principal.           |
| `core/settings_manager.py` | Gerencia presets, defaults e persistência do `settings.json`.    |
| `core/clock_engine.py`     | Atualização e formatação de hora/data.                           |
| `core/quote_engine.py`     | Geração e cache da citação diária via Groq.                      |
| `core/audio_manager.py`    | Gerenciamento centralizado de músicas, ambientes e notificações. |
| `ui/main_window.py`        | Organização da janela, painel lateral e integração geral.        |
| `ui/clock_widget.py`       | Renderização dos textos e aplicação dinâmica de estilos.         |
| `ui/settings_panel.py`     | Controles de tema, áudio, volumes e animações do painel.         |

Fluxo principal:

```txt
ClockEngine → atualiza horário
SettingsPanel → altera configurações
AudioManager → controla reprodução sonora
MainWindow → sincroniza interface e estilos
```

---

# Como executar

## Requisitos

* Python 3
* PySide6
* Groq SDK
* python-dotenv

Dentro da pasta `neoclock`:

```bash
python -m venv .venv
.venv\Scripts\activate

pip install PySide6 groq python-dotenv

python main.py
```

Depois, crie um arquivo `.env` na raiz:

```env
GROQ_API_KEY=sua_chave_aqui
```

Sem uma chave válida, o sistema de citações pode utilizar mensagens locais de fallback.

---

# Estrutura de pastas

```txt
neoclock/
  main.py

  core/
    clock_engine.py
    quote_engine.py
    settings_manager.py
    audio_manager.py

  ui/
    main_window.py
    clock_widget.py
    settings_panel.py

  assets/
    themes/
      presets.json

    audio/
      lo-fi-01.mp3
      rain-01.mp3
      rain-02.mp3
      ring-01.mp3

  data/
    settings.json
```

---

# Personalização rápida

## Adicionar novos temas

Edite:

```txt
neoclock/assets/themes/presets.json
```

E adicione novos objetos em `dark` ou `light`:

```json
{
  "id": "novo_tema",
  "label": "Novo Tema",
  "background_color": "#000000",
  "text_color": "#ffffff"
}
```

---

## Adicionar novas fontes

Inclua a família tipográfica na lista `FONTS` em:

```txt
neoclock/ui/settings_panel.py
```

O nome precisa corresponder a uma fonte instalada no sistema.

---

## Adicionar novos sons

Adicione novos arquivos em:

```txt
neoclock/assets/audio/
```

Depois registre os novos sons no `AudioManager` e no painel de configurações.

---

# Objetivo do projeto

O MyClock não pretende competir com aplicações completas de produtividade ou players de música.

A ideia é mais simples:

criar uma presença visual confortável no desktop — algo leve, silencioso, agradável e personalizável o suficiente para permanecer aberto durante longos períodos sem cansar visualmente.

---

# Licença

O projeto segue os termos definidos no arquivo `LICENSE`.

Integrações externas, como a API da Groq, continuam sujeitas aos limites e políticas dos respectivos serviços.

---

*README atualizado de acordo com o estado atual do projeto. Conforme novas funcionalidades forem adicionadas, essa documentação continuará evoluindo junto com a aplicação.*
