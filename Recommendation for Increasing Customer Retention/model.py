'''
제품에 대한 선호(카트, 결제)가 있는 경우 사용자 기반 협업필터링(CF+KNN)으로 추천
제품에 대한 선호가 없는 경우 bestseller 위주 추천
'''

# 라이브러리 import
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 데이터 불러오기
df = pd.read_csv(r'/Users/arden/Desktop/codestates/CP2/data/ratings_new.csv') # 선호도(카트담기, 구매)
prd = pd.read_csv(r'/Users/arden/Desktop/codestates/CP2/data/prd.csv') # 제품 메타정보
cst = pd.read_csv(r'/Users/arden/Desktop/codestates/CP2/data/cst.csv') # 고객 메타정보
prd = prd.set_index('product_id')
gender = cst.groupby('gender')['customer_id'].unique()

# 제품에 대한 선호가 있는 고객에게는 CF+KNN 기반 추천
class Recommend:
    def __init__(self, df, user_id, n_items=30):
        self.df = df
        self.user_id = user_id
        self.n_items = n_items
        self.neighbor_size = 20

    # 데이터 전처리
    def preprocessing(self):
        if len(self.df) > 10000: # 데이터가 많으면 필터링 후 생성
            self.df = self.df[['customer_id', 'gender', 'product_id', 'rating']]

            # 메모리 문제 방지 위해 필터링 기준 설정
            # 고객당 제품 평가 횟수
            user = self.df.groupby('customer_id').agg({'rating':np.size})
            user_cut = int(user['rating'].mean()) # quantile(0.75)
            # 제품당 평가된 횟수
            item = self.df.groupby('product_id').agg({'rating':np.size})
            item_cut = int(item['rating'].mean())

            # 3분위수 이상의 유저, 제품만 필터링
            user.loc[user['rating']>=user_cut, 'heavy'] = 1
            user_filter = user[user['heavy']==1]
            item.loc[item['rating']>=item_cut, 'heavy'] = 1
            item_filter = item[item['heavy']==1]

            # 필터링 결과 적용
            self.df_filter = self.df.loc[df['customer_id'].isin(list(user_filter.index))]
            self.df_filter = self.df_filter.loc[self.df_filter['product_id'].isin(list(item_filter.index))]
        else:
            self.df_filter = self.df
        return self.df_filter

    # rating matrix 생성
    def rating_matrix(self):
        # 같은 성별의 
        self.rating_mtx = self.df_filter.pivot(index='customer_id', columns='product_id', values='rating').fillna(0)
        return self.rating_mtx

    # 코사인 유사도 계산
    # 데이터가 큰 경우 반으로 갈라 계산
    def sim(self):
        if len(self.rating_mtx) > 20000:
            cut = int(self.rating_mtx.shape[0]/2)+1
            rating_mtx1 = self.rating_mtx[:cut]
            rating_mtx2 = self.rating_mtx[cut:]

            user_sim1 = cosine_similarity(rating_mtx1, rating_mtx1)
            user_sim1 = pd.DataFrame(user_sim1, index=rating_mtx1.index, columns=rating_mtx1.index)
            user_sim2 = cosine_similarity(rating_mtx2, rating_mtx2)
            user_sim2 = pd.DataFrame(user_sim2, index=rating_mtx2.index, columns=rating_mtx2.index)
            self.user_sim = pd.concat([user_sim1, user_sim2], axis=0)
            return self.user_sim
        else:
            self.user_sim = cosine_similarity(self.rating_mtx, self.rating_mtx)
            self.user_sim = pd.DataFrame(self.user_sim, index=self.rating_mtx.index, columns=self.rating_mtx.index)
            return self.user_sim

    # CF + KNN 시행
    def cf_knn(self, product_id):
        if product_id in self.rating_mtx:
            # 해당 사용자와 다른 사용자 간의 similarity 가져오기
            sim_score = self.user_sim[self.user_id]

            # 해당 제품에 대한 모든 사용자의 rating값 가져오기
            prd_rating = self.rating_mtx[product_id]

            # 해당 제품을 평가하지 않은 사용자의 index 가져오기
            no_rating_idx = prd_rating[prd_rating.isnull()].index

            # 해당 제품을 평가하지 않은 사용자의 rating(null) 제거
            prd_rating = prd_rating.drop(no_rating_idx)

            # 해당 제품을 평가하지 않은 사용자의 유사도값 제거
            sim_score = sim_score.drop(no_rating_idx)

            # KNN
            if self.neighbor_size == 0: # neighbor size가 지정되지 않은 경우
                # 해당 제품을 평가한 모든 사용자의 가중평균 값 구하기
                self.mean_rating = np.dot(sim_score, prd_rating) / sim_score.sum()
            else: # neighbor size가 지정된 경우
                # 지정된 neighbor size 값과 해당 제품을 평가한 총 사용자 수 중 작은 것으로 결정
                self.neighbor_size = min(self.neighbor_size, len(sim_score))

                # arrary로 변환(argsort를 사용하기 위함)
                sim_score = np.array(sim_score)
                prd_rating = np.array(prd_rating)

                # 유사도를 순서대로 정렬
                user_idx = np.argsort(sim_score)

                # 유사도를 neighbor size만큼 받기
                sim_score = sim_score[user_idx][-self.neighbor_size:]

                # 제품 rating을 neighbor size만큼 받기
                prd_rating = prd_rating[user_idx][-self.neighbor_size:]

                # 최종 예측값 계산
                self.mean_rating = np.dot(sim_score, prd_rating) / sim_score.sum()
        
        else:
            self.mean_rating = 2
        return self.mean_rating


    # 추천리스트 생성
    def rec(self):
        # 현재 사용자의 모든 아이템에 대한 예상 평점 계산
        predictions = []
        if self.user_id in self.rating_mtx.index:
            rated_index = self.rating_mtx.loc[self.user_id][self.rating_mtx.loc[self.user_id]>0].index # 이미 평가했는지 여부 확인
            items = self.rating_mtx.loc[self.user_id].drop(rated_index) # 이미 평가(경험)한 제품 제거

            # 예상평점 계산
            for item in items.index:
                self.mean_rating = self.cf_knn(item)
                predictions.append(self.mean_rating)

            candidate = pd.Series(data=predictions, index=items.index, dtype=float)
            candidate = candidate.sort_values(ascending=False)
            self.rec_items = prd.loc[candidate.index]
        else:
            self.rec_items = pd.DataFrame()
        return self.rec_items
    
    # 추천리스트 필터링
    def final_rec(self):
        # 성별
        if self.user_id in list(gender[1]): # 남자이면 pruduct_gender가 남자거나 unisex인 상품 추천
            gender_items = self.rec_items[(self.rec_items['product_gender']=='Men') | (self.rec_items['product_gender']=='Unisex')]

        else:
            gender_items = self.rec_items[(self.rec_items['product_gender']=='Women') | (self.rec_items['product_gender']=='Unisex')][:self.n_items]

                    
        self.final_items = pd.DataFrame()
        cat_lst = ['Accessories', 'Apparel', 'Footwear', 'Sporting Goods', 'Home']
        for c in cat_lst:
            cat_items = gender_items[gender_items['mainCategory']==c]
            if len(cat_items) == 0:
                continue
            elif len(cat_items) < 5:
                self.final_items = pd.concat([self.final_items, cat_items], axis=0)
            else:
                self.final_items = pd.concat([self.final_items, cat_items[:5]], axis=0)
        return self.final_items

# 제품에 대한 선호가 없는 고객을 위해 베스트셀러 추천
class Bestseller:
    def __init__(self, df, user_id, n_items=30):
        self.df = df
        self.user_id = user_id
        self.n_items = n_items
    
    def bestseller(self):
        self.df = df[['customer_id', 'product_id', 'rating']]
        # 제품별 평균 평점
        rating_mean = df.groupby('product_id')['rating'].mean()
        # 제품별 평가횟수
        rating_cnt = df.groupby('product_id')['rating'].count().sort_values(ascending=False)
        rating_cnt.columns = ['product_id', 'count']
        # 합치기
        self.bestseller = pd.merge(rating_cnt, rating_mean, left_index=True, right_index=True, how='left')
        self.bestseller.columns = ['count', 'rating']
        # 평가횟수가 높으면서 평균평점이 높은 순으로 정렬
        self.bestseller = self.bestseller.sort_values(by=['count','rating'], ascending=False)
        return self.bestseller
    
    def rec(self):
        # 다양한 카테고리의 상품 추천 위해 동일 카테고리 중복치 제거
        candidate = prd.loc[self.bestseller.index]
        self.rec_items = candidate.drop_duplicates(subset=['mainCategory', 'subCategory'], keep='first')
        return self.rec_items
    
    def final_rec(self):
        # 성별에 따라 필터링
        if self.user_id in list(gender[1]):
            gender_items = self.rec_items[(self.rec_items['product_gender']=='Men') | (self.rec_items['product_gender']=='Unisex')][:self.n_items]
        else:
            gender_items = self.rec_items[(self.rec_items['product_gender']=='Women') | (self.rec_items['product_gender']=='Unisex')][:self.n_items]
            
        self.final_items = pd.DataFrame()
        cat_lst = ['Accessories', 'Apparel', 'Footwear', 'Sporting Goods', 'Home']
        for c in cat_lst:
            cat_items = gender_items[gender_items['mainCategory']==c]
            if len(cat_items) == 0:
                continue
            elif len(cat_items) < 5:
                self.final_items = pd.concat([self.final_items, cat_items], axis=0)
            else:
                self.final_items = pd.concat([self.final_items, cat_items[:5]], axis=0)
        return self.final_items

       
# 전체 실행
def main(df, user_id, n_items):
    if user_id in df['customer_id'].values:
        r = Recommend(df, user_id, n_items)
        r.preprocessing()
        r.rating_matrix()
        r.sim()
        r.rec()
        final_items = r.final_rec()
    else:
        b = Bestseller(df, user_id)
        b.bestseller()
        b.rec()
        final_items = b.final_rec()
    return final_items  

user_id = int(input('user_id를 입력하세요'))
n_items = 30 # 30개의 아이템 추천
final_list = main(df, user_id, n_items)
print(final_list)








