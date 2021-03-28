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
│── data                    // Output data directory
│   ├── comments_data.xlsx
│   ├── posts_data.xlsx
│   ├── tag_comments_data.xlsx
│   └── tag_posts_data.xlsx
└── pics                   // Pics of posts
   ├── posts_pics             // pics of one's posts 
   └── tag_posts_pics         // pics of posts of a tag
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
        author_id = "<Author ID>"
        task_fetch_posts(author_id, 1000, f'data/{author_id}.xlsx')
        task_download_resources(f'data/{author_id}.xlsx', 'display_image_url', ['short_code'], out_dir=f'pics/{author_id}', overwrite=False)
        task_download_resources(f'data/{author_id}.xlsx', 'video_url', ['short_code'], out_dir=f'videos/{author_id}', overwrite=False)
    
        tag_name = '<Tag Name>'
        task_fetch_tag_posts(tag_name, 1000, f'data/{tag_name}.xlsx')
        task_download_resources(f'data/{tag_name}.xlsx', 'display_image_url', ['short_code'], out_dir=f'pics/{tag_name}', overwrite=False)
   ```
   
2. Run tasks in `instagram/instagram.py`.
    ```bash
   $ python -m instagram.instagram
    ```

## LICENSE
Copyright (c) 2021 Tishacy.  
Licensed under the MIT License.
