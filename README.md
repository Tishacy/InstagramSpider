# Instagram Spider

## Project structure
```
InstagramSpider
├── README.md               // Descriptions
├── LICENSE                 // License file
├── requirements.txt        // Dependencies 
├── config.ini              // Config file
├── instagram               // Source code directory
│   ├── __init__.py
│   ├── common.py               // Global variables
│   ├── instagram.py            // Core tasks 
│   ├── parser.py               // Parser classes
│   ├── query.py                // Query class
│   └── test.py                 // Test functions
└── data                    // Output data directory
    ├── comments_data.xlsx
    ├── posts_data.xlsx
    ├── tag_comments_data.xlsx
    └── tag_posts_data.xlsx
```

## Usage

1. Install dependencies of the project.  
   ```bash
   $ pip install -r requirements.txt
   ```

2. Run tasks in `instagram/instagram.py`.
    ```bash
   $ python -m instagram.instagram
    ```

## Modify tasks

1. Modify the tasks in `instagram/instagram.py`.

    ```python
    # ...
   
    if __name__=="__main__":
        task_fetch_posts_and_comments("586319507", 28, 'data/posts_data.xlsx', 'data/comments_data.xlsx')
        task_fetch_tag_posts_and_comments("pringles", 100, 'data/tag_posts_data.xlsx', 'data/tag_comments_data.xlsx')
    ```
   
2. Run tasks in `instagram/instagram.py`.
    ```bash
   $ python -m instagram.instagram
    ```

## LICENSE
Copyright (c) 2021 Tishacy.  
Licensed under the MIT License.
