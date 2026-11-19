# Publicar para teste no celular

1. Entre em https://dashboard.render.com e conecte sua conta GitHub.
2. Selecione New > Web Service e o repositório rlucca2014/Projetos_AI.
3. Use Branch: main e Root Directory: hotel-canino.
4. Runtime: Python 3. Build Command: python --version. Start Command: python backend/server.py.
5. Variável de ambiente HOST = 0.0.0.0. A variável PORT é fornecida pelo Render.
6. Selecione Free para um teste descartável e crie o serviço.
7. Espere o estado Live. Use a URL HTTPS exibida pelo Render no celular ou envie para o testador. O computador local pode ficar desligado.

Não é GitHub Pages: este aplicativo precisa executar Python, além de servir o React.

## Dados de teste

O código publicado não inclui o banco local nem os cadastros existentes. A demonstração começa vazia. Ainda não existe login: qualquer pessoa com o endereço pode consultar e alterar os cadastros. Use somente dados fictícios no teste público.

No plano Free, o SQLite fica em armazenamento temporário e pode ser perdido em reinícios ou publicações. Para preservar os dados, use um serviço pago com disco persistente, monte-o em /var/data e configure HOTEL_DB_PATH=/var/data/hotel.db. Confira os custos no provedor antes de contratar. Outra etapa possível é migrar o banco para PostgreSQL e implementar login antes do uso real.

Fontes: https://render.com/docs/web-services e https://render.com/docs/free e https://render.com/docs/disks.
