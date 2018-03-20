# coding: UTF-8
import math
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import MeCab

# ファイルから記事データを取得
def main():
	data = open("result.txt", "r").read()
	text_list = data.split(',')

	 text_num = len(text_list)

	# 文書dの単語の出現回数を格納するための配列
	fv_tf = []
	# 単語tの出現文書数を格納するための辞書
	fv_df = {}
	# 単語tの総出現回数を格納するための配列
	word_count = []
	# 文書dの単語の特徴量を格納するための配列
	fv_tf_idf = []
	# tv_dfを計算する上で必要なフラグを格納するための辞書
	count_flag = {}

	# 文書dの形態素解析と、単語tの出現回数の計算
	for txt_id, txt in enumerate(text_list):
		# MeCabを使うための初期化
		tagger = MeCab.Tagger()
		tagger.parse('')
		node = tagger.parseToNode(txt)

		# 単語tの出現回数を格納するための辞書
		fv = {}
		# 文書dの単語の総出現回数
		words = 0

		for word in fv_df.keys():
			count_flag[word] = False
		while node.next:
			node = node.next

			# 形態素解析により得られた単語
			surface = node.surface

			words += 1

			# fvにキー値がsurfaceの要素があれば1を加えなければ新しくキー値がsurfaceの要素を辞書に加え、値を1にする
			fv[surface] = fv.get(surface, 0) + 1

			# fv_dfにキー値がsurfaceの要素があれば
			if surface in fv_df.keys():

				# フラグを確認し、falseであれば
				if count_flag[surface] == False:

					# 出現文書数を1増やす
					fv_df[surface] += 1

					# フラグをTrueにする
					count_flag[surface] = True

			# fv_dfにキー値がsurfaceの要素がなければ
			else:

				# 新たにキー値がsurfaceの要素を作り値として1を代入する
				fv_df[surface] = 1

				# フラグをTrueにする
				count_flag[surface] = True

		fv_tf.append(fv)
		word_count.append(words)

	# tf, idf, tf-idfなどの計算
	for txt_id, fv in enumerate(fv_tf):
		tf = {}
		idf = {}
		tf_idf = {}
		for key in fv.keys():

		# tfの計算
			tf[key] = float(fv[key]) / word_count[txt_id]

			# idfの計算
			idf[key] = math.log(float(text_num) / fv_df[key])

			# tf-idfその他の計算
			tf_idf[key] = (tf[key] * idf[key], tf[key], idf[key], fv[key], fv_df[key])

		# リストを降順ソート
		tf_idf = sorted(tf_idf.items(), key=lambda x:x[1][0], reverse=True)
		fv_tf_idf.append(tf_idf)

	# 出力
	for txt_id, fv in enumerate(fv_tf_idf):
		for word, tf_idf in fv:
			print('%s\ttf-idf:%lf\ttf:%lf\tidf:%lf\tterm_count:%d\tdocument_count:%d' % (word, tf_idf[0], tf_idf[1], tf_idf[2], tf_idf[3], tf_idf[4]))

 main()
