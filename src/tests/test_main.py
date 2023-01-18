def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


class TestQuotes():
    API_QUOTES_ROOT = "/api/v1/quotes"

    author_ok = "Miguel de Cervantes"
    author_not_ok = "Diego Gamboa"

    quote_id_ok = "37aUWcuNWjSh"
    quote_id_not_ok = "AAAAAABBBBBB"
    quote_id_not_ok_num = 1

    quote_tag_ok = "famous-quotes"
    quote_tag_x2_ok = "sports,humorous"
    quote_tag_x2_not_ok = "will,fail"
    quote_tag_not_ok = "laGenteEstaMuyloca"

    quotes_count = 20

    def test_random(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/random")
        assert response.status_code == 200

    def test_random_ignore_qry_params(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/random?ummm=its-OK")
        assert response.status_code == 200

    def test_random_wrong_url(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/randommmm")
        assert response.status_code == 404

    def test_author(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/author/{self.author_ok}")
        assert response.status_code == 200

    def test_author_not_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/author/{self.author_not_ok}")
        assert response.status_code == 404

    def test_quote_by_id_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/by/{self.quote_id_ok}")
        assert response.status_code == 200

    def test_quote_by_id_not_ok_num_value(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/by/{self.quote_id_not_ok_num}")

        assert response.status_code == 422

    def test_quote_by_id_not_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/by/{self.quote_id_not_ok}")
        assert response.status_code == 404

    def test_quote_tags_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/tags/{self.quote_tag_ok}")
        assert response.status_code == 200

    def test_quote_tags_list_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/tags/{self.quote_tag_x2_ok}")
        assert response.status_code == 200

    def test_quote_tags_list_not_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/tags/{self.quote_tag_x2_not_ok}")
        assert response.status_code == 404

    def test_quote_tags_not_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/tags/{self.quote_tag_not_ok}")
        assert response.status_code == 404

    def test_quotes(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/")
        assert response.status_code == 200

    def test_quotes_wrong_url(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/{self.quote_tag_not_ok}")
        assert response.status_code == 404

    def test_quotes_count(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/?limit={self.quotes_count}")
        assert response.status_code == 200
        assert len((response.json())) == self.quotes_count

    def test_quotes_count_not_ok(self, test_app):
        response = test_app.get(f"{self.API_QUOTES_ROOT}/?limit={self.quotes_count}")
        assert response.status_code == 200
        assert len((response.json())) != (self.quotes_count * 2)
