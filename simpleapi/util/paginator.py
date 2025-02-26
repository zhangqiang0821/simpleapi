from sqlalchemy import func


class Paginator:
    def __init__(self, query):
        self.query = query
        self.data = None
        self.page = None
        self.limit = None

    def paginate(self, page: int, page_size: int, max_per_page=500):
        """分页查询"""
        if page_size is None:
            page_size = 20

        if page is None or page <= 0:
            raise ValueError("page or page size is None!")

        if max_per_page and page_size > max_per_page:
            raise ValueError("per page size exceeded the max limit!")

        offset = page_size * (page - 1)
        self.page = page
        self.limit = page_size
        self.data = self.query.slice(offset, offset + page_size).all()
        return self

    @property
    def total(self):
        count_stmt = self.query.statement.with_only_columns(
            func.count(), maintain_column_froms=True
        ).order_by(None)
        cnt = self.query.session.execute(count_stmt).scalar()
        return cnt

    def agg(self, cols: list):
        stmt = self.query.statement.with_only_columns(*cols, maintain_column_froms=True).order_by(
            None
        )
        ret = self.query.session.execute(stmt).first()
        return ret

    @property
    def items(self):
        return self.data

