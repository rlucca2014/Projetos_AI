# Titio Cachorrão — Hotel canino

Aplicação React + Python. Cadastro de cães e tutores, reservas, check-in/check-out, diária configurável (inicialmente R$ 110/noite), relatórios e identificação simulada por coleira.

Site: https://titio-cachorrao.onrender.com/

## Executar localmente

Requer Python 3.10 ou superior.

```powershell
python -m pip install -r requirements.txt
python backend/server.py
```

Abra http://localhost:4180. Sem DATABASE_URL, o sistema usa SQLite em backend/hotel.db. Com DATABASE_URL, usa PostgreSQL. O React está incluído nos arquivos locais.

## Banco persistente na nuvem

A versão publicada usa PostgreSQL da Neon. A conexão fica na variável DATABASE_URL, configurada em Render > titio-cachorrao > Environment. Usuário e senha não devem ser colocados no código, em commits ou no chat.

O backend lê essa variável em backend/server.py. Na Neon, consulte os detalhes em projeto titio-cachorrao > Postgres > Connect. Use uma conexão com SSL. Se a conexão PostgreSQL falhar, o aplicativo não muda silenciosamente para SQLite.

No Render, configure:

- Root Directory: hotel-canino
- Build Command: pip install -r requirements.txt
- Start Command: python backend/server.py
- HOST: 0.0.0.0
- DATABASE_URL: conexão PostgreSQL da Neon (valor secreto).

PORT é fornecida pelo Render. O armazenamento PostgreSQL fica separado do servidor: reiniciar o Render não remove os registros. Mantenha backups; persistência não substitui backup.

## Operação

Cadastre o cão e o tutor, reserve entrada/saída e registre check-in e check-out. Reservas conflitantes do mesmo cão são recusadas. A simulação de coleira identifica o cadastro; não realiza check-out automaticamente.

Relatórios e diárias mostra noites reservadas × diária da estadia. Mudanças de diária valem para novas reservas; cada estadia conserva seu preço. Pagamentos e descontos ainda não são registrados.

## Limites

Ainda não há login ou controle de acesso. Use dados fictícios na demonstração pública. A identificação física por hardware ainda não foi implementada. A versão local SQLite é independente dos cadastros da Neon.

Documentos adicionais: docs/AUTOMACAO.md e docs/PUBLICAR.md.

