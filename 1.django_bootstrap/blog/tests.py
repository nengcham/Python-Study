from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='password')
        self.user_obama = User.objects.create_user(username='obama', password='password')
        self.user_obama.is_staff = True
        self.user_obama.save()
        self.category_programing = Category.objects.create(name='programing', slug='programing')
        self.category_music = Category.objects.create(name='music', slug='music')
        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        # create post
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다',
            content='테스트 첫 번째 포스트!!!',
            category=self.category_programing,
            author=self.user_trump,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트 입니다',
            content='테스트 두 번째 입니다!!!!!',
            category=self.category_music,
            author=self.user_obama,
        )
        self.post_003 = Post.objects.create(
            title='세 번째 포스트 입니다',
            content='테스트 세 번째 입니다!!!!! 카테고리 없음!!',
            author=self.user_obama,
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_obama,
            content='첫 댓글 입니다.'
        )

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programing.name} ({self.category_programing.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn('미분류 (1)', categories_card.text)

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):
        # 1. 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        # 블로그페이지 접속 체크
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # 네비바, 카테고리 체크
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        # main-area 체크
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)

        # 2. 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):

        # 1.2 그 Post의 url은 'blog/1/'이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트 url로 접근하면 정상작동 한다(status.code, 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 2.3 첫 번째 포스트의 title이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programing.name, post_area.text)

        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)
        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)

        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)

    def test_category_page(self):
        # 1. 카테고리 페이지 접속 체크
        response = self.client.get(self.category_programing.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # 2. BeautifulSoup으로 파싱 후 네비바, 카테코리카드, 뱃지 체크
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)
        self.assertIn(self.category_programing.name, soup.h1.text)

        # 3. main-area에 programing 이름 체크, 해당 포스트만 있는지 체크
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programing.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        # 비 로그인시 status code != 200
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff가 아닌 유저가 로그인
        self.client.login(username='trump', password='password')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff인 유저가 로그인
        self.client.login(username='obama', password='password')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Post form 만들기',
                'content': 'Post Form 페이지를 만들어봅시다',
                'tags_str': 'new tag; 한글 태그, python'
            }
        )
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, 'Post form 만들기')
        self.assertEqual(last_post.author.username, 'obama')

        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # 로그인 하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(username='trump', password='password')
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        # 작성자(obama)가 접근하는 경우
        self.assertEqual(self.post_003.author, self.user_obama)
        self.client.login(username='obama', password='password')
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url,
            {
                'title': '세 번째 포스트를 수정',
                'content': '테스트 테스트',
                'category': self.category_music.pk,
                'tags_str': '파이썬 공부; 한글 태그, some tag',
            },
            follow=True
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정', main_area.text)
        self.assertIn('테스트 테스트', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)

    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

        # 로그인 하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertIn('Log in and leave a comment', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))

        # 로그인 한 상태
        self.client.login(username='obama', password='password')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment', comment_area.text)

        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content': '오바마의 댓글입니다.'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)

        new_comment = Comment.objects.last()
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)

        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('오바마의 댓글입니다', new_comment_div.text)

    def test_comment_update(self):
        comment_by_trump = Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        # obama로 로그인 한 상태
        self.client.login(username='obama', password='password')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertTrue(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')

        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)

        response = self.client.post(
            '/blog/update_comment/1/',
            {
                'content': '오바마의 댓글을 수정합니다.'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn('오바마의 댓글을 수정합니다.', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)

        def test_comment_delete(self):
            comment_by_trump = Comment.objects.create(
                post=self.post_001,
                author=self.user_trump,
                content='트럼프의 댓글입니다'
            )
            self.assertEqual(Comment.objects.count(), 2)
            self.assertEqual(self.post_001.comment_set.count(), 2)

            # 로그인 하지 않은 상태
            response = self.client.get(self.post_001.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')

            comment_area = soup.find('div', id='comment-area')
            self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
            self.assertFalse(comment_area.find('a', id='comment-2-delete-btn'))

            # trump로 로그인 한 상태
            self.client.login(username='trump', password='somepassword')
            response = self.client.get(self.post_001.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')

            comment_area = soup.find('div', id='comment-area')
            self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
            self.assertTrue(comment_area.find('a', id='comment-2-delete-btn'))

            comment_002_delete_modal_btn = comment_area.find('a', id='comment-2-delete-btn')
            self.assertIn('delete', comment_002_delete_modal_btn.text)
            self.assertEqual(
                comment_002_delete_modal_btn.attrs['data-target'],
                '#deleteCommentModal-2'
            )

            delete_comment_modal_002 = soup.find('div', id='deleteCommentModal-2')
            self.assertIn('Are You Sure?', delete_comment_modal_002.text)
            really_delete_btn_002 = delete_comment_modal_002.find('a')
            self.assertIn('Delete', really_delete_btn_002.text)
            self.assertEqual(really_delete_btn_002.attrs['href'], '/blog/delete_comment/2/')

            response = self.client.get('/blog/delete_comment/2/', follow=True)
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')

            self.assertIn(self.post_001.title, soup.title.text)
            comment_area = soup.find('div', id='comment-area')
            self.assertNotIn('트럼프의 댓글입니다', comment_area.text)

            self.assertEqual(Comment.objects.count(), 1)
            self.assertEqual(self.post_001.comment_set.count(), 1)





