local p = {}
 
local CharData = mw.loadData( 'Module:FactionScript/data' )

local function get_tenno ( word, para )
	if (para == nil or para == '') then para = 1 end
	return CharData["TennoChar"][word][para]
end

local function scale_img ( img_size, client_size )  --not implemented
	return math.ceil((img_size/20)*client_size) --template: scale_img(CharData["TennoChar"][char_list[i]][3], size)
end

local function get_img (file_name, file_size)
	if file_size == nil then file_size = '&nbsp;' end
	file_name = '[[File:'..file_name..'|'..file_size..'|link=]]'
	return file_name
end

local function gen_vowel_stack (vowels) --see sandbox css 
	local vowel_stack = '<div class="stack_content">'..vowels..'</div>'
	return vowel_stack
end

local function gen_consonant_stack (consonants)
	local consonant_stack = '<div class="stack_content">'..consonants..'</div>'
	return consonant_stack
end

local function gen_diagonal_stack ( vowels_consonants )
	local diagonal_stack = '<div class="tennoscript_stack">'..vowels_consonants..'</div>'
	return disgonal_stack
end

local function gen_horizontal_stack ( symbols )
	local horizontal_stack = '<div class="tennoscript_stack"><div class="stack_content">'..symbols..'</div></div>'
	return horizontal_stack
end

function p.tenno( frame )
	local humanwords = string.lower(frame.args[1])
	local size = frame.args[2]
	if (size == nil or size == '') then size='16' end
	local char_list = {}
	local diagonal_gen = {}
	local final_gen = {}
	local i=1
	local j=1
	while i<=string.len(humanwords) do
		local first_char = humanwords:sub(i,i)
		local second_char = humanwords:sub(i+1,i+1)
		local third_char = humanwords:sub(i+2,i+2)
		if(
		first_char == "t" or first_char == "d" or first_char == "s" or --check lua if accept (t,d,s...)
		first_char == "z" or first_char == "c" or first_char == "k" or 
		first_char == "i" or first_char == "u") then
			if second_char == "h" then
				table.insert(char_list,first_char.."h")
				i=i+2
			else
				table.insert(char_list,first_char)
				i=i+1
			end
		elseif first_char == ("n") then
			if second_char == "g" then
				table.insert(char_list,"ng")
				i=i+2
			else
				table.insert(char_list,"n")
				i=i+1
			end
		elseif  first_char == ("e") then
			if second_char == ("e" or "h") then
				table.insert(char_list,"e"..second_char)
				i=i+2
			else 
				table.insert(char_list,"e")
				i=i+1
			end
		elseif first_char == ("a") then
			if second_char == ("w" or "e") then
				table.insert(char_list,"a"..second_char)
				i=i+2
			elseif second_char == ("y") then
				table.insert(char_list,"aye")
				i=i+3
			else
				table.insert(char_list,"a")
				i=i+1
			end
		elseif first_char == ("o") then
			if second_char == ("o" or "w") then
				table.insert(char_list,"o"..second_char)
				i=i+2
			else 
				table.insert(char_list,"o")
				i=i+1
			end
		elseif CharData["TennoChar"][first_char] ~= nil then
				table.insert(char_list,first_char)
			i=i+1
		else
			table.insert(char_list,"&nbsp;")
			i=i+1
		end
	end
--end combining phonetic characters and building character list
--start generating div stacks for tenno script
	while char_list[j+1] ~= nil do
		if CharData["TennoChar"][char_list[j]][2] == "symbol" then
			local symbol_list = {}
				while CharData["TennoChar"][char_list[j]][2] == "symbol" do
					table.insert(symbol_list, get_img(CharData["TennoChar"][char_list[j]][1]))
					j=j+1
				end
			table.insert(final_gen,gen_horizontal_stack(table.concat(symbol_list)))
		elseif CharData["TennoChar"][char_list[j]][2] == "vowel" then
			local vowel_list = {}
				while CharData["TennoChar"][char_list[j]][2] == "vowel" do
					table.insert(vowel_list, get_img(CharData["TennoChar"][char_list[j]][1]))
					j=j+1
				end
			table.insert(diagonal_gen,gen_vowel_stack(table.concat(vowel_list)))
		elseif CharData["TennoChar"][char_list[j]][2] == "consonant" then
			local consonant_list = {}
				while CharData["TennoChar"][char_list[j]][2] == "consonant" do
					table.insert(consonant_list, get_img(CharData["TennoChar"][char_list[j]][1]))
					j=j+1
				end
			table.insert(diagonal_gen,gen_consonant_stack(table.concat(consonant_list))) --once loop hits a consonant
			table.insert(final_gen,gen_diagonal_stack(table.concat(diagonal_gen))) --gen diagonal stack and push to final stack
			diagonal_gen = {} --clean diagonal stack
		else
			local nil_list = {}
				while CharData["TennoChar"][char_list[j]][2] == nil do
					table.insert(nil_list, '&nbsp;')
					j=j+1
				end
		if diagonal_gen ~= nil then -- if diagonal_gen ain't empty, then there are vowels in it.
			table.insert(vowel_list, get_img(CharData["TennoChar"][char_list[j]][1]))
			table.insert(diagonal_gen,gen_vowel_stack(table.concat(vowel_list)))
			table.insert(final_gen,gen_diagonal_stack(table.concat(diagonal_gen)))
		end
			table.insert(final_gen,gen_horizontal_stack(table.concat(nil_list)))
		end
			
	end
		return table.concat(final_gen)
	end

return p
