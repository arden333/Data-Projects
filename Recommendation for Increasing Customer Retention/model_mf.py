import pandas as pd
import numpy as np

# 데이터 불러오기
df = pd.read_csv(r'/Users/arden/Desktop/codestates/CP2/data/ratings_new.csv') # 선호도(카트담기, 구매)
prd = pd.read_csv(r'/Users/arden/Desktop/codestates/CP2/data/prd.csv') # 제품 메타정보
prd = prd.set_index('product_id')
cst = pd.read_csv(r'/Users/arden/Desktop/codestates/CP2/data/cst.csv') # 고객 메타정보
gender = cst.groupby('gender')['customer_id'].unique()

# 데이터 전처리
def rating_mtx(df):    
    df = df[['customer_id', 'gender', 'product_id', 'rating']]

    # 메모리 문제 방지 위해 필터링 기준 설정
    # 고객당 제품 평가 횟수
    user = df.groupby('customer_id').agg({'rating':np.size})
    user_cut = int(user['rating'].mean()) # quantile(0.75)
    # 제품당 평가된 횟수
    item = df.groupby('product_id').agg({'rating':np.size})
    item_cut = int(item['rating'].mean())

    # 3분위수 이상의 유저, 제품만 필터링
    user.loc[user['rating']>=user_cut, 'heavy'] = 1
    user_filter = user[user['heavy']==1]
    item.loc[item['rating']>=item_cut, 'heavy'] = 1
    item_filter = item[item['heavy']==1]

    # 필터링 결과 적용
    df_filter = df.loc[df['customer_id'].isin(list(user_filter.index))]
    df_filter = df_filter.loc[df_filter['product_id'].isin(list(item_filter.index))]

    # rating_matrix 생성
    rating_mtx = df_filter.pivot(index='customer_id', columns='product_id', values='rating').fillna(0)
    return rating_mtx

#SGD
class MatrixFactorization():
    def __init__(self, R, k, learning_rate, reg_param, epochs, verbose=False):
        """
        :param R: rating matrix
        :param k: latent parameter
        :param learning_rate: alpha on weight update
        :param reg_param: beta on weight update
        :param epochs: training epochs
        :param verbose: print status
        """
        self._R = R
        self._num_users, self._num_items = R.shape
        self._k = k
        self._learning_rate = learning_rate
        self._reg_param = reg_param
        self._epochs = epochs
        self._verbose = verbose


    def fit(self):
        """
        training Matrix Factorization : Update matrix latent weight and bias

        참고: self._b에 대한 설명
        - global bias: input R에서 평가가 매겨진 rating의 평균값을 global bias로 사용
        - 정규화 기능. 최종 rating에 음수가 들어가는 것 대신 latent feature에 음수가 포함되도록 해줌.

        :return: training_process
        """

        # init latent features
        self._P = np.random.normal(size=(self._num_users, self._k))
        self._Q = np.random.normal(size=(self._num_items, self._k))

        # init biases
        self._b_P = np.zeros(self._num_users)
        self._b_Q = np.zeros(self._num_items)
        self._b = np.mean(self._R[np.where(self._R != 0)])

        # train while epochs
        self._training_process = []
        for epoch in range(self._epochs):
            # rating이 존재하는 index를 기준으로 training
            xi, yi = self._R.nonzero()
            for i, j in zip(xi, yi):
                self.gradient_descent(i, j, self._R[i, j])
            cost = self.cost()
            self._training_process.append((epoch, cost))

            # print status
            if self._verbose == True and ((epoch + 1) % 10 == 0):
                print("Iteration: %d ; cost = %.4f" % (epoch + 1, cost))

    def cost(self):
        """
        compute root mean square error
        :return: rmse cost
        """

        # xi, yi: R[xi, yi]는 nonzero인 value를 의미한다.
        # 참고: http://codepractice.tistory.com/90
        xi, yi = self._R.nonzero()
        # predicted = self.get_complete_matrix()
        cost = 0
        for x, y in zip(xi, yi):
            cost += pow(self._R[x, y] - self.get_prediction(x, y), 2)
        return np.sqrt(cost/len(xi))


    def gradient(self, error, i, j):
        """
        gradient of latent feature for GD

        :param error: rating - prediction error
        :param i: user index
        :param j: item index
        :return: gradient of latent feature tuple
        """

        dp = (error * self._Q[j, :]) - (self._reg_param * self._P[i, :])
        dq = (error * self._P[i, :]) - (self._reg_param * self._Q[j, :])
        return dp, dq


    def gradient_descent(self, i, j, rating):
        """
        graident descent function

        :param i: user index of matrix
        :param j: item index of matrix
        :param rating: rating of (i,j)
        """

        # get error
        prediction = self.get_prediction(i, j)
        error = rating - prediction

        # update biases
        self._b_P[i] += self._learning_rate * (error - self._reg_param * self._b_P[i])
        self._b_Q[j] += self._learning_rate * (error - self._reg_param * self._b_Q[j])

        # update latent feature
        dp, dq = self.gradient(error, i, j)
        self._P[i, :] += self._learning_rate * dp
        self._Q[j, :] += self._learning_rate * dq


    def get_prediction(self, i, j):
        """
        get predicted rating: user_i, item_j
        :return: prediction of r_ij
        """
        return self._b + self._b_P[i] + self._b_Q[j] + self._P[i, :].dot(self._Q[j, :].T)

    def get_complete_matrix(self):
        """
        computer complete matrix PXQ + P.bias + Q.bias + global bias

        - PXQ 행렬에 b_P[:, np.newaxis]를 더하는 것은 각 열마다 bias를 더해주는 것
        - b_Q[np.newaxis:, ]를 더하는 것은 각 행마다 bias를 더해주는 것
        - b를 더하는 것은 각 element마다 bias를 더해주는 것

        - newaxis: 차원을 추가해줌. 1차원인 Latent들로 2차원의 R에 행/열 단위 연산을 해주기위해 차원을 추가하는 것.

        :return: complete matrix R^
        """
        return self._b + self._b_P[:, np.newaxis] + self._b_Q[np.newaxis:, ] + self._P.dot(self._Q.T)
    

# rating matrix 생성
rating_mtx = rating_mtx(df)
rating_mtx_arr = rating_mtx.to_numpy() # array형태로 변환

# 학습
mf = MatrixFactorization(rating_mtx_arr, k=20, learning_rate=0.01, reg_param=0.01, epochs=50, verbose=True)
mf.fit()
pred_mtx = mf.get_complete_matrix()
pred_mtx = pd.DataFrame(pred_mtx, index=rating_mtx.index, columns=rating_mtx.columns)


# 추천
class Recommend:
    def __init__(self, pred_mtx, user_id, n_items=30):
        self.pred_mtx = pred_mtx
        self.user_id = user_id
        self.n_items = n_items

    def rec(self):
        candidate = self.pred_mtx.loc[self.user_id].sort_values(ascending=False)
        self.rec_items = prd.loc[candidate.index][:self.n_items]
        return self.rec_items

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

def main(user_id, pred_mtx=pred_mtx, n_items=30):
    r = Recommend(pred_mtx, user_id, n_items)
    r.rec()
    final_items = r.final_rec()
    return final_items

final_list = main(3)
print(final_list)

