for prop1 in [nil, :テイル, :タ, :連用...] do
  for prop2 in [nil, :テイル, :タ, :連用...] do
    for prop3 in [nil, :テイル, :タ, :連用...] do
       try do
         print(HB3.basic {[prop1, prop2, prop3, "たべる"].reverse.filter { |x| x != nil }.reduce {
           |x, y| [x, y]
         }})
       catch do
         print("error")
       end
    end
 end
end
