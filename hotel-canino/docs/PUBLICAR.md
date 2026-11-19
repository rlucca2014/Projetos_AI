# Publicação com PostgreSQL persistente

A versão atual está em https://titio-cachorrao.onrender.com/ e usa Neon PostgreSQL.

No Render: Root Directory hotel-canino; Build Command pip install -r requirements.txt; Start Command python backend/server.py; HOST=0.0.0.0. PORT é definida pelo Render.

Configure DATABASE_URL como variável secreta em Environment, usando a conexão obtida em Neon > projeto titio-cachorrao > Postgres > Connect. Não copie a conexão para arquivos versionados. A aplicação cria suas tabelas automaticamente sem apagar dados existentes.

O plano Free do Render tem disco temporário. Por isso a versão pública usa o banco externo da Neon. Sem DATABASE_URL, o sistema usa SQLite, adequado para execução local, mas que não deve ser usado para persistência no Render Free.

O site ainda não possui login: use apenas dados fictícios no teste público. Configure autenticação e backups antes de uso real. Os limites dos planos gratuitos continuam sujeitos aos provedores.

