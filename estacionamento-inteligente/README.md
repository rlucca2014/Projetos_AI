# Parkwise — protótipo de estacionamento

Painel web demonstrativo para administrar 300 vagas organizadas em seis setores (A a F), com 50 vagas por setor.

## Abrir a aplicação

Abra `index.html` em um navegador moderno. Não requer instalação ou servidor. As alterações de estado das vagas são salvas no armazenamento local do navegador.

## Recursos

- Indicadores de vagas livres, ocupadas e taxa de ocupação.
- Mapa com vista isométrica 3D estilizada e vista em planta.
- Clique em uma vaga para selecioná-la; use o botão de detalhes para alternar entre livre e ocupada.
- Navegação pelos setores A–F, busca por identificador e atividade recente.
- Layout adaptado para desktop e celular.

## Dados de demonstração

Os estados iniciais são gerados para demonstração. Cada navegador mantém seus próprios estados em `localStorage`; portanto, os dados não são compartilhados entre dispositivos. O histórico de alterações existe apenas durante a sessão aberta.

## Estrutura

- `index.html` — aplicação completa, sem dependências externas de build.
- `docs/INTEGRACAO-ESP32.md` — proposta de integração futura com ESP32-S3 e backend Python.

## Próxima etapa

A conexão com sensores e o backend Python ainda não foram implementados. O documento de integração define identificadores estáveis (`A-01` a `F-50`), um modelo de evento e rotas sugeridas para orientar essa etapa.
