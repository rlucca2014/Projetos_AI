# Identificação e automação

## Fluxo recomendado

Cadastro do cão e tutor → reserva de datas → associação do código da coleira → identificação na recepção → confirmação de check-in → registro de movimentações → confirmação de entrega ao tutor → check-out.

## Piloto: coleira com RFID/NFC

Uma tag passiva em acessório próprio para coleira é aproximada do leitor na recepção. O código identifica o cão e abre sua estadia. Evita procurar e digitar nomes; a aproximação e a confirmação ainda são ações humanas. A distância de leitura depende do padrão, tag e leitor. NFC de aproximação não é um portal de passagem.

## Passagem automática

Um portal RFID UHF pode identificar tags sem aproximação manual, mas exige projeto e teste no local. Use duas zonas de leitura ou sensores de passagem para inferir direção; uma detecção isolada não comprova entrada/saída. Validar alcance, vários cães juntos, leituras através de paredes, repetição e impacto do corpo do animal na leitura. Registre eventos com ID único, leitor, tag, direção e horário; deduplique e mantenha fila offline. Leitura desconhecida ou ambígua deve gerar pendência.

Bluetooth BLE com gateways pode indicar presença aproximada, mas proximidade de sinal não garante passagem pela porta. Bateria, posição e interferência devem ser monitoradas. ESP32-S3 pode participar como gateway BLE ou controlador de um leitor externo compatível; ele não é um leitor RFID UHF por si só.

## AirTag

A Apple apresenta AirTag como localizador de objetos pessoais via Buscar. Seus identificadores Bluetooth mudam e há mecanismos contra rastreamento indesejado. Não há integração implementada neste projeto. Não adotar como controlador principal de check-in/check-out do hotel.

## Movimentação não é encerramento da estadia

Saída para passeio, banho ou pátio deve ser um evento de movimentação separado. O checkout definitivo deve depender de entrega ao tutor e autorização do operador. A automação pode identificar e sugerir a operação, sem decidir sozinha que a estadia terminou.

## API do protótipo

- GET /api/state: cães, estadias e últimas leituras.
- POST /api/dogs: name, breed, owner, phone, tag, notes.
- POST /api/stays: dog_id, start, end (datas ISO).
- POST /api/transition: id da estadia; reserved → present → departed.
- POST /api/scan: tag. Apenas simulação, sem autenticação de hardware.

Para hardware real, criar endpoint separado autenticado, HTTPS, idempotência, validação de leitor e auditoria. Não expor este servidor local diretamente na internet.

## Fontes

- Apple: https://support.apple.com/en-mide/109021
- Apple: https://www.apple.com/newsroom/2021/04/apple-introduces-airtag/
- Avigilon, leitores RFID e proximidade: https://www.avigilon.com/access-control/door-readers

A arquitetura de portal e o fluxo operacional acima são propostas de projeto e precisam de validação física antes de aquisição em escala.
