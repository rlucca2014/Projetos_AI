# Integração futura com ESP32-S3

Este documento descreve uma proposta para a próxima etapa. **A integração com sensores, o backend Python e a API ainda não estão implementados nesta versão.** Hoje a aplicação usa dados demonstrativos e `localStorage` no navegador.

## Identificação das vagas

Use um identificador fixo por vaga, igual ao exibido no mapa:

- Setores: `A` a `F`.
- Vagas por setor: `01` a `50`.
- Exemplos: `A-01`, `C-24`, `F-50`.
- Total: 300 vagas.

Cada sensor físico deve ser associado a exatamente um desses identificadores. Guarde essa relação no backend, sem depender da ordem em que os sensores se conectam.

## Arquitetura proposta

1. O ESP32-S3 lê o sensor instalado na vaga e determina se há um veículo.
2. O dispositivo envia o estado e seu identificador a um backend Python (por exemplo, FastAPI).
3. O backend valida o dispositivo, grava o último estado e a hora da leitura.
4. A interface consulta a API e recebe atualizações em tempo real por WebSocket ou Server-Sent Events.

Para uma implantação com muitos dispositivos, MQTT é uma opção para transportar eventos; HTTP também pode ser suficiente para um primeiro piloto. A decisão depende do sensor, da rede e da infraestrutura disponíveis.

## Modelo de evento sugerido

```json
{
  "space_id": "A-01",
  "occupied": true,
  "device_id": "esp32-a01",
  "observed_at": "2026-11-13T12:00:00Z"
}
```

`occupied` deve representar o estado atual detectado. O backend deve validar a associação `device_id` → `space_id`, rejeitar IDs desconhecidos e registrar quando cada sensor foi visto pela última vez.

## Rotas de API sugeridas

| Método | Rota | Uso |
| --- | --- | --- |
| `GET` | `/api/spaces` | Listar as 300 vagas e seus estados atuais. |
| `GET` | `/api/spaces/{space_id}` | Consultar uma vaga. |
| `PATCH` | `/api/spaces/{space_id}` | Alterar manualmente o estado por um operador autenticado. |
| `POST` | `/api/sensor-events` | Receber uma leitura do ESP32-S3. |
| `GET` | `/api/events` | Fluxo de atualizações, se for usada a opção SSE. |
| `WS` | `/api/ws` | Atualizações em tempo real, se for usado WebSocket. |

As rotas são uma proposta de contrato, não endpoints existentes.

## Cuidados para a implementação

- Autenticar os dispositivos; não aceitar atualização anônima de estado.
- Usar HTTPS fora de uma rede local controlada e proteger as credenciais.
- Tratar sensores sem conexão como **sem comunicação**, em vez de presumir que a vaga está livre.
- Debounce/histerese para evitar alternância causada por leituras instáveis.
- Manter `observed_at` e `last_seen_at` para distinguir estado antigo de vaga livre.
- Definir como resolver conflito entre sensor e alteração manual.
- Começar com poucas vagas e validar sensores, rede e posicionamento antes de instalar em 300 vagas.
