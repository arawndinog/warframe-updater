function p.tenno_test1 ( frame )
	local humanwords = string.lower(frame.args[1])
	local size = frame.args[2]
		if (size == nil or size == '') then size='16' end
	local char_list = {}
	local tennobet_list = {}
	local i=string.len(humanwords)
	while i>0 do
		local this_char = humanwords:sub(i,i)
		local prev_char = humanwords:sub(i-1,i-1)
		if this_char == "h" then
			if (prev_char == "t" or
				prev_char == "d" or
				prev_char == "s" or
				prev_char == "z" or
				prev_char == "c" or
				prev_char == "k" or
				prev_char == "i" or
				prev_char == "e" or
				prev_char == "u") then
				table.insert(char_list,prev_char.."h")
				i=i-2
			else
				table.insert(char_list,"h")
				i=i-1
			end
		elseif this_char == "g" then
			if prev_char == "n" then
				table.insert(char_list,"ng")
				i=i-2
			else
				table.insert(char_list,"g")
				i=i-1
			end
		elseif  this_char == "e" then
			if humanwords:sub(i-2,i-2)..prev_char == "ay" then
				table.insert(char_list,"aye")
				i=i-3
			elseif (prev_char == "e" or
					prev_char == "a") then
				table.insert(char_list,prev_char.."e")
				i=i-2
			else 
				table.insert(char_list,"e")
				i=i-1
			end
		elseif this_char == ("w") then
			if (prev_char == "a" or
				prev_char == "o") then
				table.insert(char_list,prev_char.."w")
				i=i-2
			else
				table.insert(char_list,"oo")
				i=i-1
			end
		elseif this_char == ("o") then
			if prev_char == "o" then
				table.insert(char_list,"oo")
				i=i-2
			else 
				table.insert(char_list,"o")
				i=i-1
			end
		elseif CharData["TennoChar"][this_char] ~= nil then
				table.insert(char_list,this_char)
			i=i-1
		else
			table.insert(char_list,"&nbsp;")
			i=i-1
		end
	end
	
	local j=#char_list
	while j>0 do
		table.insert(tennobet_list,char_list[j])
		j=j-1
	end
	return table.concat(tennobet_list,",")
end