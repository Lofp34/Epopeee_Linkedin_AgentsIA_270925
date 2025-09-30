Le MCP Recherche d'entreprises est un serveur qui permet d'interagir avec l'API de recherche d'entreprises françaises de data.gouv.fr. Vous pouvez effectuer :

-   **Recherches textuelles** : Trouvez des entreprises françaises selon divers critères tels que le nom, l'activité et la localisation
-   **Recherches géographiques** : Localisez des entreprises autour de points géographiques spécifiques en utilisant la latitude, la longitude et des filtres de rayon

## MCP Recherche d'entreprises

Ce MCP (Module de Connexion à une API) permet d'interagir avec l'API Recherche d'entreprises mise à disposition par data.gouv.fr.

## Description

L'API Recherche d'entreprises permet de rechercher et de trouver des entreprises françaises. Elle offre deux types de recherche :

-   Recherche textuelle (dénomination, adresse, dirigeants et élus)
-   Recherche géographique

## Fonctionnalités

Le MCP permet de :

-   Rechercher des entreprises par différents critères
-   Filtrer les résultats selon plusieurs paramètres
-   Accéder aux informations essentielles des entreprises (dénomination, SIREN, SIRET, code NAF)
-   Effectuer des recherches géographiques autour d'un point avec les paramètres suivants :
    -   Latitude et longitude du point de recherche
    -   Rayon de recherche (jusqu'à 50km)
    -   Filtres d'activité (code NAF, section d'activité)
    -   Pagination des résultats

## Source

Ce MCP est basé sur l'API officielle de data.gouv.fr : [API Recherche d'entreprises](https://www.data.gouv.fr/fr/dataservices/api-recherche-dentreprises/)

## Limitations

L'API comporte certaines limitations :

-   Ne donne pas accès aux prédécesseurs et successeurs d'un établissement
-   Ne permet pas d'accéder aux entreprises non-diffusibles
-   Ne permet pas d'accéder aux entreprises qui se sont vues refuser leur immatriculation au RCS
-   Le rayon de recherche géographique est limité à 50km maximum

## Limites techniques

-   Limite de 7 appels par seconde
-   Disponibilité : 100% sur le mois dernier
-   Accès : Ouvert à tous

## Utilisation

#### En tant qu'utilisateur

Le moyen le plus simple d'utiliser ce MCP est via `npx` :

```
<span><span>npx</span><span> mcp-recherche-entreprises</span></span>
```

#### En tant que développeur

1.  Installation des dépendances :

2.  Build du projet :

Cette commande va :

-   Compiler les fichiers TypeScript en JavaScript
-   Les placer dans le dossier `dist/`
-   Rendre les fichiers JavaScript exécutables

3.  Démarrage :

Pour lancer le serveur en mode développement avec l'Inspector MCP (recommandé pour le développement) :

Pour lancer le serveur sans l'Inspector :

L'Inspector MCP fournit une interface graphique pour tester et déboguer les requêtes MCP en temps réel.

#### Utilisation avec Cursor

Pour utiliser ce MCP dans Cursor, ajoutez la configuration suivante dans votre fichier `.cursor/settings.json` :

JSON

```
<span><span>{</span></span>
<span><span>  "mcpServers"</span><span>: {</span></span>
<span><span>    "recherche-entreprises"</span><span>: {</span></span>
<span><span>      "command"</span><span>: </span><span>"npx mcp-recherche-entreprises"</span></span>
<span><span>    }</span></span>
<span><span>  }</span></span>
<span><span>}</span></span>
```

Cette configuration permettra à Cursor d'utiliser automatiquement ce MCP pour les recherches d'entreprises.

## Ressources MCP pour les contributeurs

### Documentation officielle

-   [Documentation MCP](https://modelcontextprotocol.io/docs)
-   [Spécification MCP](https://modelcontextprotocol.io/spec)
-   [Exemples de serveurs](https://modelcontextprotocol.io/examples)

### Outils de développement

-   [SDK TypeScript MCP](https://github.com/modelcontextprotocol/typescript-sdk)
-   [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Outil de débogage et d'analyse

### Bonnes pratiques

-   Utiliser le SDK TypeScript pour l'implémentation
-   Suivre les conventions de code du projet
-   Implémenter une gestion d'erreur robuste
-   Documenter clairement l'API
-   Maintenir la compatibilité avec les versions futures

### Tests et débogage

-   Utiliser l'Inspector pour le débogage
-   Implémenter des tests unitaires
-   Vérifier la conformité avec la spécification MCP
-   Analyser les performances avec les outils appropriés

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! Consultez notre guide de contribution pour plus d'informations sur la façon de contribuer à ce projet.

![avatar](https://github.com/ThinkBeDo.png)

GoHighLevel MCP 服务器，用于 Claude 桌面版和 ChatGPT 集成。需要从 GoHighLevel 获取的私有集成 API 密钥，并通过环境变量进行配置。

![avatar](https://github.com/amazonbusiness.png)

Amazon Business Integrations MCP Server fournit des outils pour accéder à la documentation des API Amazon Business, rechercher du contenu et des solutions pour les cas d'utilisation courants d'intégration B2B.

![avatar](https://github.com/trevSmart.png)

由 IBM 开发的 MCP 服务器，为您的 IDE AI 代理提供 Salesforce 组织上下文。需要 Node.js v22.7.0 或更高版本。内部测试需要连接到组织的 Salesforce CLI。

![avatar](https://github.com/dayal-arnav05.png)

一个 MCP 服务器实现，集成了 Claude 与 Salesforce，支持与您的 Salesforce 数据和元数据进行自然语言交互。支持 Salesforce 对象和字段管理、数据查询、Apex 代码管理等功能。

![avatar](https://github.com/sooperset.png)

Le serveur Model Context Protocol (MCP) pour les produits Atlassian (Confluence et Jira). Prend en charge les déploiements Cloud ainsi que Server/Data Center. Distribué sous forme d'image Docker. Configurez via des variables d'environnement pour l'authentification et le filtrage.

![avatar](https://github.com/priyapanigrahy.png)

Une implémentation de serveur MCP intégrant Claude avec Salesforce pour des interactions en langage naturel avec les données et métadonnées Salesforce. Prend en charge l'authentification Salesforce via des variables d'environnement pour le nom d'utilisateur/mot de passe ou le flux OAuth 2.0 avec les identifiants client.

![MCP server config](https://registry.npmmirror.com/@lobehub/assets-fileicon/1.0.0/files/assets/file.svg)

MCP server config

```
<span><span>{</span></span>
<span><span>  "mcpServers"</span><span>: {</span></span>
<span><span>    "yoanbernabeu-mcp-recherche-entreprises"</span><span>: {</span></span>
<span><span>      "args"</span><span>: [</span></span>
<span><span>        "mcp-recherche-entreprises"</span></span>
<span><span>      ],</span></span>
<span><span>      "command"</span><span>: </span><span>"npx"</span></span>
<span><span>    }</span></span>
<span><span>  }</span></span>
<span><span>}</span></span>
```

## Table des matières